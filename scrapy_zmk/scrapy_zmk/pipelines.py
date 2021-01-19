# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import scrapy
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join


class SaveItemPipeline:
    def process_item(self, item, spider):
        # if 'next_url' in item.keys():
        #     yield scrapy.Request(item['next_url'],
        #                             meta={
        #                                 'dont_redirect': True,
        #                                 'handle_httpstatus_list': [301, 302]
        #                             })
        # save
        # return item
        print('SaveItemPipeline')


class MyFilesPipeline(FilesPipeline):
    '''
    FCK
    (False, <twisted.python.failure.Failure scrapy.pipelines.files.FileException: >)
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, headers=self.headers)

    def file_path(self, request, response=None, info=None, *, item=None):
        path = urlparse(request.url).path
        temp = join(basename(dirname(path)), basename(path))
        return f'{basename(dirname(path))}/{basename(path)}'

    def item_completed(self, results, item, info):
        print(results)
        return item
