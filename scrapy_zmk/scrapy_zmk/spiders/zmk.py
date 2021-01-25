# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_zmk.items import ScrapyZmkItem
from bs4 import BeautifulSoup
import hashlib
import time


class ZmkSpider(scrapy.Spider):
    name = 'zmk'
    allowed_domains = ['zimuku.la', 'zmk.pw']
    start_urls = []
    ua = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}

    def start_requests(self):
        index = 125042 # index = 1
        while index < 30000:
            url = f'http://www.zimuku.la/detail/{index}.html'
            print(f'at {index}: # {url}')
            item = ScrapyZmkItem()
            item['index'] = index
            yield scrapy.Request(url, headers=self.ua, meta={'item': item})
            index += 1
            time.sleep(5)

    def parse(self, response):
        item = response.meta['item']
        
        soup = BeautifulSoup(response.text, 'lxml')
        item['zh'], item['en'] = soup.select(
            '.md_tt')[0].a.string.split('/')[:2]
        sub_name = soup.select('.md_tt')[0].h1['title']
        suffix = ''
        if sub_name[-1] == 'rar' or sub_name[-1] == 'srt' or sub_name[-1] == 'zip' or sub_name[-1] == 'ass' or sub_name[-1] == '7z':
            suffix = sub_name[-1]
        item['suffix'] = suffix

        yield scrapy.Request(f"http://zmk.pw/dld/{item['index']}.html",
                             headers=self.ua,
                             callback=self.parse_dld, 
                             meta={'item': item})

    def parse_dld(self, response):
        item = response.meta['item']

        # xp = response.xpath('/html/body/main/div/div/div/table/tbody/tr/td[1]/div/ul/li[5]/a')
        soup = BeautifulSoup(response.text, 'lxml')
        _dld_url = 'http://zmk.pw' + \
            soup.select('.down')[0].find_all(
                name='li')[-2].a['href']  # 备用下载通道（二）

        self.ua['Referer'] = f"http://zmk.pw/dld/{item['index']}.html"
        yield scrapy.Request(_dld_url,
                             meta={
                                 'dont_redirect': True,
                                 'handle_httpstatus_list': [301, 302],
                                 'item': item,
                             },
                             headers=self.ua,
                             callback=self.parse_download)


    def parse_download(self, response):
        item = response.meta['item']
        print(f"{item['index']}:", response.headers['location'].decode('ascii'))

        hash_object = hashlib.sha1(
            response.headers['location'])
        item['sha1'] = hash_object.hexdigest()
        
        item['file_urls'] = [
            response.headers['location'].decode('ascii')]  # 下载文件url
        
        print(item)

        return item
