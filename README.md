本项目用于测试`click` 包的使用，通过click包将爬虫任务封装为命令行快捷指令，爬取基金行情数据，存入文件并展示
### 
### 一.安装
`pip install -r requirements.txt`

`pip install --editable .`
​

### 二.使用

- 准备数据

将需要关注的基金6位数编码写入`funds.txt` （分行填写）

- 命令行操作

`savefund` 将基金数据爬取到`results.txt`文件中

`showfund` 在命令行显示基金数据
​

### 三.文件说明
`chromedriver`         用于爬虫爬取数据

`fund.py`                  主要代码，将爬虫任务封装成命令行命令

`funds.txt`               基金编码文件

`requirements.txt`  项目依赖

`results.txt`           数据结果存储文件

`setup.py`                 用于将命令打包

​

