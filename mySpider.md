# Scrapy

Scrapy 是用 Python 实现的一个为了爬取网站数据、提取结构性数据而编写的应用框架，常应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。

## 简介

![scrapy](scrapy.png)

* Scrapy Engine(引擎): 负责Spider、ItemPipeline、Downloader、Scheduler中间的通讯，信号、数据传递等。
* Scheduler(调度器): 它负责接受引擎发送过来的Request请求，并按照一定的方式进行整理排列，入队，当引擎需要时，交还给引擎。
* Downloader（下载器）：负责下载Scrapy Engine(引擎)发送的所有Requests请求，并将其获取到的Responses交还给Scrapy Engine(引擎)，由引擎交给Spider来处理，
* Spider（爬虫）：它负责处理所有Responses,从中分析提取数据，获取Item字段需要的数据，并将需要跟进的URL提交给引擎，再次进入Scheduler(调度器).
* Item Pipeline(管道)：它负责处理Spider中获取到的Item，并进行进行后期处理（详细分析、过滤、存储等）的地方。
* Downloader Middlewares（下载中间件）：你可以当作是一个可以自定义扩展下载功能的组件。
* Spider Middlewares（Spider中间件）：你可以理解为是一个可以自定扩展和操作引擎和Spider中间通信的功能组件（比如进入Spider的Responses;和从Spider出去的Requests）

## 执行流程

1. 引擎：Hi！Spider, 你要处理哪一个网站？
2. Spider：老大要我处理xxxx.com。
3. 引擎：你把第一个需要处理的URL给我吧。
4. Spider：给你，第一个URL是xxxxxxx.com。
5. 引擎：Hi！调度器，我这有request请求你帮我排序入队一下。
6. 调度器：好的，正在处理你等一下。
7. 引擎：Hi！调度器，把你处理好的request请求给我。
8. 调度器：给你，这是我处理好的request
9. 引擎：Hi！下载器，你按照老大的下载中间件的设置帮我下载一下这个request请求
10. 下载器：好的！给你，这是下载好的东西。（如果失败：sorry，这个request下载失败了。然后引擎告诉调度器，这个request下载失败了，你记录一下，我们待会儿再下载）
11. 引擎：Hi！Spider，这是下载好的东西，并且已经按照老大的下载中间件处理过了，你自己处理一下（注意！这儿responses默认是交给def parse()这个函数处理的）
12. Spider：（处理完毕数据之后对于需要跟进的URL），Hi！引擎，我这里有两个结果，这个是我需要跟进的URL，还有这个是我获取到的Item数据。
13. 引擎：Hi ！管道 我这儿有个item你帮我处理一下！调度器！这是需要跟进URL你帮我处理下。然后从第四步开始循环，直到获取完老大需要全部信息。
14. 管道调度器：好的，现在就做！

## 常用命令

```bash
> scrapy
Scrapy 2.4.1 - no active project

Usage:
  scrapy <command> [options] [args]     

Available commands:
  bench         Run quick benchmark test
  commands
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

  [ more ]      More commands available when run from project directory

Use "scrapy <command> -h" to see more info about a command
```

```bash
# 新建工程
> scrapy startproject mySpider
New Scrapy project 'mySpider' ...

# 目录结构
cd mySpider
ls|dir
mySpider/
    scrapy.cfg
    mySpider/
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/ # 爬虫目录
            __init__.py

# 生成爬虫 runoob
> scrapy genspider runoob "runoob.com"
Created spider 'runoob' using template 'basic' in module:
  mySpider.spiders.runoob

# 显示爬虫列表
> scrapy list
runoob

# 执行爬虫
> scrapy crawl runoob

# 保存数据
> scrapy crawl runoob -o noob.[json|jsonlines|jl|csv|xml|marshal|pickle]

# pipeline清洗保存数据
# 编写Pipeline
# uncomment settings.py -> ITEM_PIPELINES

```

## 下载文件

1. 编写 items.py
2. 配置setting.py的 ITEM_PIPELINES 和 FILES_STORE
3. 【可选】自定义下载 Pipeline

## 注意事项

* 下载失败 `twisted.python.failure.Failure scrapy.pipelines.files.FileException`
* `parse` 中同时出现 `yield` 和 `return` 时，pipeline失效

## 参考

<https://www.runoob.com/w3cnote/scrapy-detail.html>
