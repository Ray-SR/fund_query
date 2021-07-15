import asyncio
import datetime
import os
from concurrent import futures

import click
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


chrome_driver_path = os.path.join(os.path.dirname(__file__), "chromedriver")
results_path = os.path.join(os.path.dirname(__file__), "results")
funds_path = os.path.join(os.path.dirname(__file__), "funds")

executor = futures.ThreadPoolExecutor(max_workers=20)


async def query(code):
    """
    爬虫
    :param code: 基金编码
    :return: 基金名称，涨幅
    """
    url = f"http://fund.eastmoney.com/{code}.html"
    chrome_opt = Options()
    chrome_opt.add_argument("start-maximized")
    chrome_opt.add_argument("enable-automation")
    chrome_opt.add_argument("--headless")
    chrome_opt.add_argument("--no-sandbox")
    chrome_opt.add_argument("--disable-infobars")
    chrome_opt.add_argument("--disable-dev-shm-usage")
    chrome_opt.add_argument("--disable-browser-side-navigation")
    chrome_opt.add_argument("--disable-gpu")
    chrome_opt.add_argument("--disable-extensions")
    chrome_opt.add_argument("--dns-prefetch-disable")
    chrome_opt.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=chrome_opt, executable_path=chrome_driver_path)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, browser.get, url)
    # browser.get(url)
    print(f"success {code}")
    rate_rule = "//dl[@class='dataItem02']/dd[@class='dataNums']/span[2]/text()"
    name_rule = "//div[@class='fundDetail-tit']/div/text()"
    html_text = browser.page_source
    html_obj = etree.HTML(html_text)

    rate = html_obj.xpath(rate_rule)[0]
    name = html_obj.xpath(name_rule)[0]

    return name, rate


@click.command()
@click.argument("code", default="all")
def save(code):
    """
    保存数据
    :param code: 基金编码，默认为all,查询所有funds.txt文件中的基金数据
    :return:
    """
    click.echo(f'code is: {code}')

    data_list = []
    if code == "all":
        with open(funds_path, "rb") as f:
            code_list = f.readlines()
            if not code_list:
                click.echo("未发现基金编码数据，请在funds.txt文件中分行填写")
                return
            code_list = [code.decode().replace("\n", "") for code in code_list]
            data_list = asyncio.run(get_data(code_list))
            # print(data_list)

    else:
        name, rate = query(code)
        data_list = [(name, rate)]

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_list.insert(0, (f"最后更新时间", now))
    with open(results_path, "wb") as f:
        for data in data_list:
            text = f"{data[0]}: {data[1]}\n"
            f.write(text.encode())


async def get_data(code_list):
    task_list = [query(code) for code in code_list]
    data_list = await asyncio.gather(*task_list)
    return data_list


@click.command()
def show():
    """
    显示results.txt文件中的数据
    :return:
    """
    with open(results_path, "r") as f:
        lines = f.readlines()
        if not lines:
            click.echo("暂无数据，请使用savefund命令获取数据")
            return
        click.echo("*" * 33)
        click.echo(lines[0])
        click.echo("*" * 33)
        for line in lines[1:]:
            name = line.split(":")[0]
            rate = line.split(":")[1]
            text = f"{name}: {rate}"
            fg = "blue" if "-" in rate else "red"
            click.secho(text, fg=fg)


if __name__ == '__main__':
    save()
