# README

# Flask-Admin Dashboard Example

Basic dashboard app with Admin LTE template and Flask Admin, it has:

- User Registration
- Login as general or admin user
- Roles management
- Create form in modal window by default
- Inline editing enabled by default
- Skins and layout customization
- Dashboard, charts, chat and calendar examples

Utilities:

- AdminLTE Bootstrap template
- Flask-Security
- Flask-Admin
- A lot of Charts libraries
- SQLite

### How to use

- Clone or download the git repository. `sh $ git clone https://github.com/openpipes/pipes.git`
- Create and activate a virtual environment: `sh $ virtualenv venv $ source venv/bin/activate`
- Install the requirements inside the app folder `sh $ pip install -r requirements.txt`
- Once the process finishes give execution permission to app.py file and run it `sh $ chmod +x app.py $ ./app.py`
- The first execution will create automatically a sample sqlite database.
- Open your favorite browser and type `localhost:5568/admin` then just log in with the default user or register one.

### Screenshots

![screenshots/index.png](screenshots/index.png)

![screenshots/login.png](screenshots/login.png)

![screenshots/register.png](screenshots/register.png)

![screenshots/home.png](screenshots/home.png)

![screenshots/user.png](screenshots/user.png)

![screenshots/edit.png](screenshots/edit.png)

![screenshots/create.png](screenshots/create.png)

![screenshots/skins.png](screenshots/skins.png)

## To do list

- 统计数据
    - 访问数量
    - 用户数量
    - 文件数量
- 交互图表
    - 政策发布的时间分布
    - 政策发布的类型分布
    - 交互的中国地图
- 留言区
    - 用户给后台留言
- 模型工坊
    - toggle-tab （未做两个标签页之间的交互）
        - 模拟器
        - 变量列表
        - 模型列表
        - 运行日志
    - 变量列表
        - 复选变量
        - 批量提交变量至模拟器
    - 模型列表
        - 单选模型
        - 提交模型至模拟器
    - 模拟器
        - 删除变量
        - 修改参数
        - 运行模型
    - 运行日志
        - 显示提交过的模型
        - 下载模型的输出文件
        - 提供多种格式的输出
    - 通知栏
        - 显示系统通知
        - 显示模型运行状态的通知
    - 知识图谱
        - 嵌入neo4j的视图
        - 保存图谱的图片
        - 下载图谱中导出的数据(根据权限)
    - 数据采集(管理员) （正在做爬虫，上手之后做嵌入）
        - 嵌入crawlab的视图