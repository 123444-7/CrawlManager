# FastAPI API 文档

## 版本信息

- **API 版本**: 0.1.0
- **OpenAPI 版本**: 3.1.0

## 目录

- [获取集合数据 CSV](#获取集合数据-csv)
- [获取索引](#获取索引)
- [上传 Scrapy 项目](#上传-scrapy-项目)
- [显示 Scrapy 项目](#显示-scrapy-项目)
- [取消等待项目](#取消等待项目)
- [取消 Scrapy 项目](#取消-scrapy-项目)
- [获取运行中的 Scrapy 项目](#获取运行中的-scrapy-项目)
- [运行 Scrapy 项目](#运行-scrapy-项目)
- [列出集合](#列出集合)
- [删除集合](#删除集合)
- [获取集合数据](#获取集合数据)
- [获取计划任务](#获取计划任务)
- [取消任务](#取消任务)

## 获取集合数据 CSV

- **路径**: `/collection-data-csv`
- **HTTP 方法**: GET
- **摘要**: 获取集合数据 CSV
- **操作ID**: get_collection_data_csv_collection_data_csv_get
- **参数**:
  - `collection_name` (query, required, string): 集合名称
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 获取索引

- **路径**: `/data_view`
- **HTTP 方法**: GET
- **摘要**: 获取索引
- **操作ID**: get_index_data_view_get
- **响应**:
  - 200: 成功响应

## 上传 Scrapy 项目

- **路径**: `/upload-scrapy-project/`
- **HTTP 方法**: POST
- **摘要**: 上传 Scrapy 项目
- **操作ID**: upload_scrapy_project_upload_scrapy_project__post
- **请求体**:
  - `multipart/form-data`: 
    - `crawl_name` (string): 爬取名称
    - `project_name` (string): 项目名称
    - `command` (string): 命令
    - `table_name` (string): 表名称
    - `zip_file` (binary): 压缩文件
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 显示 Scrapy 项目

- **路径**: `/show-scrapy-projects/`
- **HTTP 方法**: GET
- **摘要**: 显示 Scrapy 项目
- **操作ID**: show_scrapy_projects_show_scrapy_projects__get
- **响应**:
  - 200: 成功响应

## 取消等待项目

- **路径**: `/cancel-waiting-project`
- **HTTP 方法**: GET
- **摘要**: 取消等待项目
- **操作ID**: cancel_waiting_project_cancel_waiting_project_get
- **参数**:
  - `dir_name` (query, required, string): 目录名称
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 取消 Scrapy 项目

- **路径**: `/cancel-scrapy-project`
- **HTTP 方法**: GET
- **摘要**: 取消 Scrapy 项目
- **操作ID**: cancel_scrapy_project_cancel_scrapy_project_get
- **参数**:
  - `dir_name` (query, required, string): 目录名称
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 获取运行中的 Scrapy 项目

- **路径**: `/running-scrapy-projects`
- **HTTP 方法**: GET
- **摘要**: 获取运行中的 Scrapy 项目
- **操作ID**: get_running_scrapy_projects_running_scrapy_projects_get
- **响应**:
  - 200: 成功响应

## 运行 Scrapy 项目

- **路径**: `/run-scrapy-project/{dir_name}/`
- **HTTP 方法**: GET
- **摘要**: 运行 Scrapy 项目
- **操作ID**: run_scrapy_project_run_scrapy_project__dir_name___get
- **参数**:
  - `dir_name` (path, required, string): 目录名称
  - `schedule_job` (query, boolean, default: false): 计划任务
  - `cron_schedule` (query, string): Cron 计划
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 列出集合

- **路径**: `/collections/`
- **HTTP 方法**: GET
- **摘要**: 列出集合
- **操作ID**: list_collections_collections__get
- **响应**:
  - 200: 成功响应

## 删除集合

- **路径**: `/delete-collection`
- **HTTP 方法**: DELETE
- **摘要**: 删除集合
- **操作ID**: delete_collection_delete_collection_delete
- **参数**:
  - `collection_name` (query, required, string): 集合名称
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 获取集合数据

- **路径**: `/collection-data/`
- **HTTP 方法**: GET
- **摘要**: 获取集合数据
- **操作ID**: get_collection_data_collection_data__get
- **参数**:
  - `collection_name` (query, required, string): 集合名称
  - `page` (query, integer, default: 1): 页数
  - `items_per_page` (query, integer, default: 10): 每页项目数
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 获取计划任务

- **路径**: `/get-scheduled-tasks`
- **HTTP 方法**: GET
- **摘要**: 获取计划任务
- **操作ID**: get_scheduled_tasks_get_scheduled_tasks_get
- **响应**:
  - 200: 成功响应

## 取消任务

- **路径**: `/cancel-task/{task_id}`
- **HTTP 方法**: GET
- **摘要**: 取消任务
- **操作ID**: cancel_task_cancel_task__task_id__get
- **参数**:
  - `task_id` (path, required, string): 任务ID
- **响应**:
  - 200: 成功响应
  - 422: 验证错误

## 模型

- `Body_upload_scrapy_project_upload_scrapy_project__post`: 上传 Scrapy 项目请求体
  - `crawl_name` (string): 爬取名称
  - `project_name` (string): 项目名称
  - `command` (string): 命令
  - `table_name` (string): 表名称
  - `zip_file` (binary): 压缩文件
- `HTTPValidationError`: HTTP 验证错误
  - `detail` (array): 详细错误信息
    - `ValidationError`: 验证错误
      - `loc` (array): 错误位置
      - `msg` (string): 错误消息
      - `type` (string): 错误类型

这是 FastAPI API 的基本文档。使用这些端点可以执行不同的操作，包括上传 Scrapy 项目、获取数据和管理任务。根据需要，您可以查看特定端点的详细信息。
