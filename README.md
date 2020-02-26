# README

Created: Dec 25, 2019 1:32 PM
Created By: Jean Ma
Last Edited Time: Feb 26, 2020 9:57 PM

# PIPES V2.0-官方主页

Pipes 是一个基于Python语言开发的项目。此项目用于针对中文政策文档的语义分析，文档整理，词源回溯etc。demo地址： 该项目正在开发中。目前可用版本是v2.1。

# To do

- admin 后期开发
- 模型工坊
- 深度优先词源回溯
- 政策分类机器学习

# Features 特性

- 支持pdf、txt、doc、docx文档读取
- 对中文文档进行排版整理，试别目录、章节标题、表格
- 对中文文档的词汇进行分割、词性标注、统计
- 对已解析的词汇进行回溯
- 对Shelve、ElasticSearch、PostgreSQL 数据库的读写
- 管理员UI，包括邮件通知机制。管理员可进行文档批量上传，数据库读取，文档编辑，模型调整等。

# Usage

- 读取文档并解析

    ```python
    import PolicyReader as pr
    value = {"title":"","url":"","cities":"","provinces":"","keywords":"","doc_type":"",
                  "publish_time":"","score":"","unit":"","hash_code":"","resume":""}
    doc = pr.read("./file",**value)

    doc.statistics()
    ```

- 解析后文档功能
    - 词源回溯

        ```python
        from PolicyReader.db import ElasticServer,DatabaseOpts
        conf = DatabaseOpts.esOpts(index="token")
        es = ElasticServer().connect(**conf)
        doc.getHead(es.to_md5(word))
        ```

- 数据库的使用
    - 同步文档到数据库

        ```python
        from PolicyReader.db import PsqlServer,ElasticServer,Shelve,DatabaseOpts
        doc.sync(database=dbname,user=user,password=password,table=tablename)
        ```

    - ElasticSearch

        ```python
        from PolicyReader.db import ElasticServer,DatabaseOpts
        conf = DatabaseOpts.esOpts(index="token")
        es = ElasticServer().connect(**conf)
        ```

    - Postgres

        ```python
        from PolicyReader.db import ElasticServer,DatabaseOpts
        articlemetadata_psql_config = DatabaseOpts.psqlOpts(database = dbname,table = tablename,password = password ,host = PSQL_HOST)
        ps = PsqlServer(** articlemetadata_psql_config)
        ```

- 文档分类（开发中）

# Architecture

# Preview

# Change Log

- V2.1
    - admin dashboard 增加功能：图表链接数据库，实现实时更新；增加外部链接跳转功能（如跳转至谷歌）；可自定义对数据库数据的批量操作功能；数据库管理界面实现分页，富文本编辑；
- V2.0
    - 增加文档排版功能
    - 增加Admin UI
    - 增加词源回溯功能
    - 增加对词的统计
    - 重构数据库
- V1.0
    - 上传文档，分词，标注

# Installation 安装、配置和运行程序

- Clone or download the git repository. `sh $ git clone https://github.com/openpipes/pipes.git`
- Create and activate a virtual environment: `sh $ virtualenv venv $ source venv/bin/activate`
- Install the requirements inside the app folder `sh $ pip install -r requirements.txt`
- Once the process finishes give execution permission to app.py file and run it `sh $ chmod +x app.py $ ./app.py`
- The first execution will create automatically a sample sqlite database.
- Open your favorite browser and type `localhost:5568/admin` then just log in with the default user or register one.

# License 版权和许可信息（或阅读许可证）

# Contact 联系信息