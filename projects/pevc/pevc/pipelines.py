# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawlab import save_item

class PevcPipeline:
    def process_item(self, item, spider):
        result = {
            'name': item['name'],
            'data_type': item['data_type'],
            'suburb': item['suburb'],
            'state': item['state'],
            'postcode': item['postcode'],
            'img_src': item['img_src'],
            'preferred_mailing': item['preferred_mailing'],
            'phone': item['phone'],
            'member_type': item['member_type'],
            'category': item['category'],
            'website': item['website'],
            'services_provided': item['services_provided'],
            'social_profiles': item['social_profiles'],
            'hashstr': item['hashstr'],
            'retrieval_data': item['retrieval_data'],
        }
        save_item(spider.name,result)
