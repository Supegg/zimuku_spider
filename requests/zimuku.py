# -*- coding: utf-8 -*-
"""
Created on 2021/1/13

@author: Supegg Rao
"""
import os
import sys
import random
import requests
import re
import logging
import time
from bs4 import BeautifulSoup


def get_work_names(html):
    """
    获取电影/美剧的中文和英文名称
    电影/美剧名称是一大类，比如一个美剧可能有几个字幕文件
    :return:
    """
    soup = BeautifulSoup(html, 'lxml')

    result = soup.select('.md_tt')[0].a.string.split('/')
    return result[0], result[1]


def get_sub_name(html):
    """
    获取字幕名称
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'lxml')
    return soup.select('.md_tt')[0].h1['title']


def url_iterator(start, end):
    """
    地址迭代器
    :param start: 开始下标
    :param end: 结束下标
    :return:
    """
    url = 'http://www.zimuku.la/detail/{}.html'
    for index in range(start, end):
        yield index, url.format(index)


def get_dld_url(number):
    """
    获取字幕文件下载地址
    :param number:
    :return:
    """
    _url = 'http://zmk.pw/dld/{}.html'.format(number)
    r = requests.get(_url, timeout=5)
    soup = BeautifulSoup(r.text, 'lxml')
    random_num = random.randint(0, 3)
    try:
        _dld_url = 'http://zmk.pw' + \
            soup.select('.down')[0].find_all(
                name='li')[-2].a['href']  # 备用下载通道（二）
    except Exception as e:
        print(e, '获取下载地址失败')
        raise Exception('获取下载地址失败')
    return _dld_url


def get_sub_content(number, url):
    """
    获取字幕文件
    :param number:
    :param url:
    :return:
    """
    headers = {
        'Referer': f"http://zmk.pw/dld/{number}.html",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    proxies_list = text_read('proxies.txt')
    proxies_len = len(proxies_list)

    global proxie_num
    global proxie_temp
    proxie_temp = proxie_temp+1
    # 每个ip每次下载的次数
    if proxie_temp == 5:
        proxie_num = (proxie_num+1) % proxies_len
        proxie_temp = 0

    proxies = {'http': 'http://{}'.format(proxies_list[proxie_num])}
    proxies_states = False
    while(not proxies_states):
        try:
            print(proxies)
            print('代理ip:', proxie_num)
            print('此ip使用的次数', proxie_temp)
            # allow_redirects=False, 301/302重定向资源的问题
            res = requests.get(url, headers=headers, stream=True,
                               proxies=proxies, timeout=5, verify=False, allow_redirects=False)
            print(res.headers['location'])

            res = requests.get(res.headers['location'], headers=headers, stream=True,
                               proxies=proxies, timeout=5, verify=False, allow_redirects=False)

            # proxie_num=(proxie_num+1)%proxies_len
            proxies_states = True
        except:
            print("Unexpected error:", sys.exc_info()[0])
            # print('该代理已过期或无法使用')
            # print('切换代理地址')
            print('代理ip:', proxie_num)
            proxie_num = (proxie_num+1) % proxies_len
            proxie_temp = 0
            proxies = {'http': 'http://{}'.format(proxies_list[proxie_num])}
            proxies_states = False
            return None

    #res = requests.get(url, headers=headers, stream=True,timeout=20,verify=False)
    if res.status_code == 404 and res.history:  # 代理的情况下需要重新用响应的url再请求一遍
        res = requests.get(res.url)
        if res.status_code != 200:
            return None

    return res.content


def get_sub_content_bjproxy(number, url):
    """
    获取字幕文件
    :param number:
    :param url:
    :return:
    """
    headers = {
        'Referer': "http://zmk.pw/dld/{}.html".format(number),
    }

    PROXY_POOL_HTTP = 'http://www.bjproxy.com/vps_server/getIpPort.do?orderCode=2018081110395839943749%20&areaCode=0&format=1'

    global proxie_num
    global proxie_temp
    proxies = {}
    # url1='https://www.baidu.com/robots.txt'
    proxies['http'] = 'http://'+requests.get(PROXY_POOL_HTTP).text
    print(proxies)

    proxies_states = False
    while(not proxies_states):
        try:
            print(proxies)
            print('代理ip:', proxie_num)
            print('此ip使用的次数', proxie_temp)
            res = requests.get(url, headers=headers, stream=True,
                               proxies=proxies, timeout=1, verify=False)
            proxies_states = True
        except requests.exceptions.ProxyError as e:
            print('该代理已过期或无法使用')
            print('切换代理地址')
            proxies['http'] = 'http://'+requests.get(PROXY_POOL_HTTP).text
            proxies_states = False

    return res.content


def save(filename, content):
    """
    保存获取到的文件
    :param filename: 获取文件名
    :param content: 文件内容
    """
    if not filename:
        print('文件名为空')
        return
    if not content:
        print('文件内容为空')
        return
    filename.replace(' ', '')
    if not os.path.exists('download'):
        os.mkdir('download')
    with open(os.path.join('download', filename), 'wb') as f:
        f.write(content)
        print('[√] file: {}, saved'.format(filename[:30]))


def text_read(filename):
    # Try to read a txt file and return a list. Return [] if there was a mistake.
    try:
        file = open(filename, 'r')
    except IOError:
        print("Unexpected error:", sys.exc_info()[0])
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]

    file.close()
    return content


def main(s, e=1000000):
    start = s
    end = e  # 147269
    global proxie_num
    for index, url in url_iterator(start, end):
        while True:
            time.sleep(random.randint(1, 5))  # 友好的爬虫
            print('---------------------------------')
            print('at : #', index)
            print(url)
            # print('代理ip:',proxie_num)
            # print('代理ip使用个数',proxie_num)
            try:  # 获取字幕详情界面
                r = requests.get(url, timeout=5, allow_redirects=False)
                if r.status_code == 302:
                    print('页面已被移除: {}'.format(url))
                    break
            except Exception as e:
                print('访问官网失败, 请检查网络: {}'.format(e))
                continue

            try:
                work_names_zh, work_names_en = get_work_names(
                    r.text)  # 获取电影/美剧名称

            except Exception as e:
                print("Unexpected error:", sys.exc_info()[0])
                continue

            print(work_names_zh, work_names_en)

            try:
                sub_name = get_sub_name(r.text)
                print('原来的标题', sub_name)
                sub_name = sub_name.split('.')
                suffix = ''
                if sub_name[-1] == 'rar' or sub_name[-1] == 'srt' or sub_name[-1] == 'zip' or sub_name[-1] == 'ass' or sub_name[-1] == '7z':
                    suffix = sub_name[-1]
                    sub_name = str(index)+'.'+sub_name[-1]
                else:
                    sub_name = str(index)

            except Exception as e:
                print("Unexpected error:", sys.exc_info()[0])
                continue

            print('修改好的标题', sub_name)
            path = "download/"
            sub_path = path+sub_name
            if os.access(sub_path, os.F_OK):
                print('该文件已存在')
                break

            try:
                _dld_url = get_dld_url(number=index)
                content = get_sub_content(number=index, url=_dld_url)

                if not None:
                    if len(content) < 1024:
                        continue
                    #content = get_sub_content_bjproxy(number=index, url=_dld_url)
                    save(sub_name, content)
                    open('start', 'wt').write(str(index))
                    open('sub_list', 'at', encoding='utf-8').write(
                        f"{index}, {work_names_zh}, {work_names_en}, {suffix}, {sub_name}\n")
                    break

            except Exception as e:
                print("Unexpected error:", sys.exc_info()[0])
                continue


if __name__ == '__main__':
    logging.basicConfig(
        format="%(levelname)s : %(message)s", level=logging.INFO)
    global proxie_num
    global proxie_temp
    global res
    proxie_temp = 0
    proxie_num = 0

    s = int(open('start').readline())+1
    print(f"start from {s}")
    main(s)
