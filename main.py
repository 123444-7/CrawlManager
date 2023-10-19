import os
import subprocess
import zipfile
import pymongo
import shutil
import multiprocessing
import psutil
import time
import csv
import tempfile
import threading
from queue import Queue
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from apscheduler.triggers.cron import CronTrigger
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 配置CORS 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 连接到MongoDB服务器
client = pymongo.MongoClient("mongodb://userName:pwd@host:post/?authSource=admin")

db = client["test"]
tasks_collection = db['scheduled_tasks']
manager = multiprocessing.Manager()
max_concurrent_processes = 1
semaphore = manager.Semaphore(max_concurrent_processes)
scheduler = BackgroundScheduler()
scheduler.start()
task_processes = {}
static_path = os.path.join(os.getcwd(), "templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
current_directory = os.getcwd()
task_queue = Queue(maxsize=1)
queue_list = []


@app.get("/collection-data-csv", response_class=FileResponse)
def get_collection_data_csv(collection_name: str):
    collection = db[collection_name]
    data = collection.find({})  # 获取全部数据

    if not data:
        # 如果没有数据，返回一个空的CSV文件
        return FileResponse("empty.csv")

    # 创建一个临时文件
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as temp_file:
        # 构建 CSV 数据
        csv_writer = csv.writer(temp_file)

        # 使用数据的第一个文档来获取表头
        header = data[0].keys()
        csv_writer.writerow(header)

        # 写入数据
        for document in data:
            csv_writer.writerow(document.values())

    # 配置响应，传递临时文件的路径
    filename = f"{collection_name}.csv"
    return FileResponse(temp_file.name, filename=filename)


def load_tasks_from_mongodb():
    tasks = tasks_collection.find()
    for task in tasks:
        job_id = task['_id']
        cron_schedule = task['cron_schedule']
        dir_name = task['dir_name']

        # 创建任务并添加到调度器
        scheduler.add_job(run_scrapy_project, trigger=CronTrigger.from_crontab(cron_schedule), args=[dir_name],
                          id=job_id)


@app.get("/data_view")
async def get_index():
    # 拼接完整的文件路径
    file_path = os.path.join(static_path, "data_view.html")

    # 使用FileResponse返回HTML文件
    return FileResponse(file_path, media_type="text/html")


@app.get("/")
async def get_index():
    os.chdir(current_directory)
    # 拼接完整的文件路径
    file_path = os.path.join(static_path, "index.html")

    # 使用FileResponse返回HTML文件
    return FileResponse(file_path, media_type="text/html")


def unzip_project(zip_path, project_name):
    #    timestamp = str(time.time())
    project_name = str(project_name)
    #    dir_str = project_name+timestamp
    #    hash_object = hashlib.md5()
    #    hash_object.update(dir_str.encode('utf-8'))
    #    dir_name = hash_object.hexdigest()
    dir_name = project_name
    extraction_dir = f"projects/{dir_name}"
    os.makedirs(extraction_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)
    current_directory = os.getcwd()
    source_file = f'{current_directory}/crawlab.py'
    target_file = f'{extraction_dir}/crawlab.py'
    shutil.copy(source_file, target_file)
    return dir_name


def insert_scrapy_project_info(dir_name, crawl_name, project_name, command, table_name):
    project_url = f"/run-scrapy-project/{dir_name}"
    if command.startswith("[") and command.endswith("]"):
        command = command.replace("[", "").replace("]", "").split(",")
    # 定义爬虫信息
    scrapy_project = {
        "dir_name": dir_name,
        "crawl_name": crawl_name,
        "project_name": project_name,
        "command": command,
        "table_name": table_name,
        "project_url": project_url,
    }
    collection = db["scrapy_projects"]
    # 插入到集合
    insert_result = collection.insert_one(scrapy_project)

    # 返回结果
    if insert_result.acknowledged:
        return {"message": "Scrapy project information inserted successfully",
                "inserted_id": str(insert_result.inserted_id)}
    else:
        return {"error": "Failed to insert Scrapy project information"}


@app.post("/upload-scrapy-project/")
async def upload_scrapy_project(
        crawl_name: str = Form(...),
        project_name: str = Form(...),
        command: str = Form(...),
        table_name: str = Form(None),
        zip_file: UploadFile = File(...)
):
    if not zip_file.filename.lower().endswith('.zip'):
        return JSONResponse(content={"error": "Invalid file format. Only .zip files are allowed."}, status_code=400)

    try:
        # 读取上传文件内容到内存
        zip_content = await zip_file.read()
        dir_name = unzip_project(BytesIO(zip_content), project_name)

        if not table_name:
            table_name = f"result_{project_name}"

        insert_result = insert_scrapy_project_info(dir_name, crawl_name, project_name, command, table_name)

        if "error" in insert_result:
            return JSONResponse(content={"error": insert_result["error"]}, status_code=500)
        else:
            return JSONResponse(content={"message": insert_result["message"]})
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to extract project: {str(e)}"}, status_code=500)


@app.get("/show-scrapy-projects/")
def show_scrapy_projects():
    # 检索爬虫信息
    collection = db["scrapy_projects"]
    cursor = collection.find({}, {"_id": 0})
    scrapy_projects = list(cursor)

    # 检查有数据
    if not scrapy_projects:
        return {"message": "No scrapy projects found in the database."}

    return {"scrapy_projects": scrapy_projects}


def terminate_process_tree(process):
    try:
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()  # 终止子进程
        parent.kill()  # 终止父进程
        parent.wait()  # 等待父进程终止
    except psutil.NoSuchProcess:
        pass  # 进程不存在


@app.get("/cancel-waiting-project")
def cancel_waiting_project(dir_name: str):
    waiting_projects = queue_list
    for project in waiting_projects:
        tmp = project[0] + "_" + project[1]
        if dir_name == tmp:
            queue_list.remove(project)
            return {"message": f"Project with dir_name {dir_name} and its child processes have been terminated."}


@app.get("/cancel-scrapy-project")
def cancel_scrapy_project(dir_name: str):
    if dir_name not in task_processes:
        return {"message": f"Project with dir_name {dir_name} is not currently running."}

    process = task_processes[dir_name]

    if process.is_alive():
        # 任务正在运行，尝试终止进程及其子进程
        terminate_process_tree(process)
        del task_processes[dir_name]
        return {"message": f"Project with dir_name {dir_name} and its child processes have been terminated."}
    else:
        # 任务已完成
        del task_processes[dir_name]
        return {"message": f"Project with dir_name {dir_name} has already finished."}


@app.get("/running-scrapy-projects")
def get_running_scrapy_projects():
    running_projects = []
    waiting_projects = []
    for project in queue_list:
        project_dict = {}
        project_dict['dir_name'] = project[0] + "_" + project[1]
        waiting_projects.append(project_dict)

    for dir_name, process in task_processes.copy().items():
        if not process.is_alive():
            # 任务已完成，从正在运行的任务列表中移除
            del task_processes[dir_name]
        else:
            # 任务仍在运行
            running_projects.append({"dir_name": dir_name})

    return {"running_scrapy_projects": running_projects, "waiting_scrapy_projects": waiting_projects}


def run_scrapy_command(dir_name, command, process_dict):
    try:
        # 切换到项目目录
        os.chdir(current_directory)
        project_dir = os.path.join("projects", dir_name)
        os.chdir(project_dir)
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        pass
    finally:
        os.chdir(current_directory)


def execute_scrapy_task(dir_name, command, task_processes):
    with semaphore:
        process = multiprocessing.Process(target=run_scrapy_command, args=(dir_name, command, task_processes))
        task_processes[dir_name + "_" + command] = process
        process.start()


@app.get("/run-scrapy-project/{dir_name}/")
def run_scrapy_project(dir_name: str, schedule_job: bool = False, cron_schedule: str = None):
    get_running_scrapy_projects()
    # 用dir_name获取项目信息
    collection = db["scrapy_projects"]
    project_info = collection.find_one({"dir_name": dir_name})
    command = project_info.get("command")
    if project_info is None:
        return JSONResponse(content={"error": f"Project with dir_name {dir_name} not found."}, status_code=404)

    # 切换到项目目录
    os.chdir(current_directory)
    project_dir = os.path.join("projects", dir_name)
    os.chdir(project_dir)

    if not schedule_job:
        # 如果不是定时任务，立即运行主要命令
        if command is None:
            return {"error": "Scrapy project not found."}
        if isinstance(command, list):
            for com in command:
                if (dir_name + "_" + com) in task_processes:
                    return {"error": "Task already running."}
                # 将任务添加到队列中
                task_queue.put((dir_name, com))
            return {"message": "Scrapy project execution started successfully."}
        else:
            if (dir_name + "_" + command) in task_processes:
                return {"error": "Task already running."}
            # 将任务添加到队列中
            task_queue.put((dir_name, command))
            return {"message": "Scrapy project execution started successfully."}

    else:
        # 如果是定时任务，添加定时任务到调度器
        try:
            scheduler.add_job(run_scrapy_project, trigger=CronTrigger.from_crontab(cron_schedule), args=[dir_name],
                              id=dir_name)
            job_id = dir_name
            task_info = {
                '_id': job_id,
                'cron_schedule': cron_schedule,
                'dir_name': dir_name
            }
            tasks_collection.insert_one(task_info)
            os.chdir(current_directory)
            return {"message": f"Scrapy job for dir_name {dir_name} scheduled successfully with CRON: {cron_schedule}"}
        except Exception as e:
            os.chdir(current_directory)
            return {"error": f"Failed to schedule Scrapy job: {str(e)}"}


# 获取数据库中所有的集合
def get_collections():
    collections = db.list_collection_names()
    collections.remove("scrapy_projects")
    collections.remove("scheduled_tasks")
    return collections


@app.get("/collections/")
def list_collections():
    collections = get_collections()
    collection_data = [
        {"collection_name": collection1, "collection_url": f"/collection-data/?collection_name={collection1}"} for
        collection1 in collections]
    return JSONResponse(content={"collections": collection_data})


@app.delete("/delete-collection")
async def delete_collection(collection_name: str):
    try:
        # 使用 collection_name 删除指定集合
        db[collection_name].drop()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# 查询集合中的数据
def query_collection_data(collection_name, page, items_per_page):
    collection = db[collection_name]
    # 计算跳过的文档数
    skip = (page - 1) * items_per_page

    # 查询当前分页需要的文档，并限制返回的数量
    cursor = collection.find().skip(skip).limit(items_per_page)

    data = [document for document in cursor]
    for document in data:
        document.pop("_id", None)
        document.pop("_tid", None)
    total_items = collection.count_documents({})
    return data, total_items


@app.get("/collection-data/", response_class=HTMLResponse)
def get_collection_data(collection_name: str, page: int = 1, items_per_page: int = 10):
    data, total_items = query_collection_data(collection_name, page, items_per_page)
    total_pages = -(-total_items // items_per_page)  # 向上取整
    paginated_data = data

    if not paginated_data:
        return JSONResponse(content={"collection_data": [], "total_pages": total_pages, "current_page": page})

    # 过滤掉 _id 和 _tid 列
    for document in paginated_data:
        document.pop("_id", None)
        document.pop("_tid", None)

    return JSONResponse(content={"collection_data": paginated_data, "total_pages": total_pages, "current_page": page})


@app.get("/get-scheduled-tasks")
def get_scheduled_tasks():
    jobs = scheduler.get_jobs()
    task_list = []
    for job in jobs:
        task_info = {
            "id": job.id,
            "next_run_time": job.next_run_time.isoformat(),
            "trigger_type": str(type(job.trigger)),
            "cancel_url": f"/cancel-task/{job.id}"
        }
        task_list.append(task_info)
    return {"tasks": task_list}


@app.get("/cancel-task/{task_id}")
def cancel_task(task_id: str):
    try:
        scheduler.remove_job(task_id)
        tasks_collection.delete_one({'_id': task_id})
        return {"message": f"Task with ID {task_id} has been canceled."}
    except Exception as e:
        return {"error": f"Failed to cancel task: {str(e)}"}


# 在应用启动时加载已存储的任务
load_tasks_from_mongodb()


def process_task_queue():
    while True:
        if not task_queue.empty():
            dir_name, command = task_queue.get()
            task_list = [dir_name, command]
            queue_list.append(task_list)
        if len(task_processes) < 3 and queue_list:
            dir_name, command = queue_list.pop(0)
            execute_scrapy_task(dir_name, command, task_processes)


# 启动处理任务队列的线程
task_queue_thread = threading.Thread(target=process_task_queue)
task_queue_thread.start()


def loading():
    while True:
        get_running_scrapy_projects()
        time.sleep(10)


loading_thread = threading.Thread(target=loading)
loading_thread.start()
