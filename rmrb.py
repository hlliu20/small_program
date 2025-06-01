# 仅供交流学习
# 爬取人民日报文章保存到.txt文件，图片保存到img文件夹
# 2025.06.01
# V1.0.0
# https://paper.people.com.cn/rmrb/pc/content/202501/01/content_30049271.html
# https://paper.people.com.cn/rmrb/pc/content/202501/01/content_30049272.html
# 思路，人民日报的url很有规律，先想着直接按文章编号爬取，从30049271开始递增
#     然后发现还要前面对应的日期时间正确
#     所以，从某天开始，从第一版开始，https://paper.people.com.cn/rmrb/pc/layout/202501/01/node_01.html
#     获取该版下文章url，通过url获取文章，然后版号递增，直到那一版404了说明超了，换下一天继续

# 应该也可以直接文章编号递增，不行了就把前面日期加一天

# 2022-2024年的url有变化
# https://paper.people.com.cn/rmrb/html/2022-01/01/nbs.D110000renmrb_01.htm
# https://paper.people.com.cn/rmrb/html/2022-01/01/nw.D110000renmrb_20220101_1-01.htm
# 日期再早的不能这样访问了

import time
from tqdm import tqdm
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    }
base_url =  "https://paper.people.com.cn/rmrb/pc"
image_num = 0


# 获取node_url下文章（标题，url）的数组
def get_title_urls(node_url):
    title_urls = []
    response = requests.get(node_url,headers=headers)
    if response.status_code == 200:
        response.encoding = "utf-8"
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        li_as = soup.select("ul.news-list li a")
        for a in li_as:
            title_urls.append((a.text.strip(), base_url + a.get("href").split("..")[-1]))
    elif response.status_code == 404:
        # 说明超了，没有这一版
        pass
    else:
        print(f"Failed to retrieve the webpage: {node_url}\nwith response code: {response.status_code}")
    return title_urls


# 下载url图片保存到save_path
def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"下载图片时发生错误: {e}")
        return False


# 获取此url下的文章、图片并保存
def get_content_from_url(url, year):
    global image_num
    res = ""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = "utf-8"
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.select_one("div.article")
        if article.find("h3").text.strip() != "":
            res += "副标题：" + article.find("h3").text.strip() + "\n"
        res += "标题：" + article.find("h1").text.strip() + "\n"
        if article.find("h2").text != "":
            res += "副标题："
            for p in article.select("h2 p"):
                res += p.text.strip() + "  "
        if article.find("h4"):
            res += "作者：" + article.find("h4").text.strip() + "\n"
        res += "来源：" + article.select_one("span").text.strip().replace("\xa0", " ") + "\n"
        if article.select("div.attachment div"):
            res += "attachment：\n"
            atta_img = article.select("div.attachment img")
            atta_div = article.select("div.attachment div")
            if len(atta_div) == len(atta_img):
                for i in range(len(atta_img)):
                    div = atta_div[i]
                    img = atta_img[i]
                    img_url = base_url + img.get("src").split("..")[-1]
                    img_path = Path(f"{year}/img/{image_num:04}.{img_url.split('.')[-1]}")
                    if download_image(img_url, img_path):
                        res += f"{image_num:04}.{img_url.split('.')[-1]}\n"
                        image_num += 1
                    else:
                        res += "图片下载失败\n"
                    for p in div.select("p"):
                        res += p.text.replace("\xa0", " ").replace("\u2002", "  ").replace("\u3000", "  ") + "\n"
            else:
                for div in atta_div:
                    for p in div.select("p"):
                        res += p.text.replace("\xa0", " ").replace("\u2002", "  ").replace("\u3000", "  ") + "\n"
                    res += "\n"
                for img in atta_img:
                    img_url = base_url + img.get("src").split("..")[-1]
                    img_path = Path(f"{year}/img/{image_num:04}.{img_url.split('.')[-1]}")
                    if download_image(img_url, img_path):
                        res += f"{image_num:04}.{img_url.split('.')[-1]}\n"
                        image_num += 1
        res += "正文：\n"
        for p in article.select("div#ozoom p"):
            res += p.text.replace("\xa0", " ").replace("\u3000", "  ") + "\n"
    else:
        print(f"Failed to retrieve the webpage: {url}\nwith response code: {response.status_code}\n{response.text}")
    return res


# 获取date这一天的人民日报文章
def load_RMRB_day(date):
    middle_url = date.strftime("/layout/%Y%m/%d/")
    # node_num = 20 if is_workday(date) else 8
    file = Path(date.strftime(f"%Y/%Y_%m_%d.txt"))
    res = f"{file}\n"
    if not file.parent.exists():
        file.parent.mkdir(parents=True, exist_ok=True)  # parents=True 表示递归创建，exist_ok=True 表示如果目录已存在不会报错
    for i in range(1,21):
        node_url = base_url + middle_url + f"node_{i:02}.html"
        title_urls = get_title_urls(node_url)
        if not title_urls:
            break
        res += f"#{i:02}版\n"
        for (title,url) in title_urls:
            content = get_content_from_url(url,date.year)
            if not content:
                print(f"title:{title}\nurl:{url}\n获取失败")
                with open("errors.txt", "w+", encoding="utf-8") as f:
                    f.write(f"#get_content_from_url_error\ntitle:{title}\nurl:{url}\n")
                continue
            res += content + "\n"
    with open(file, "w", encoding="utf-8") as f:
        f.write(res)


# 获取从date_start到date_end的人民日报文章
def load_RMRB_from_to(date_start, date_end):
    dates = []
    while date_start <= date_end:
        dates.append(date_start)
        date_start += timedelta(days=1)
    for date in tqdm(dates, desc="Processing Dates", unit="date"):
        load_RMRB_day(date)
        time.sleep(10) # 每爬一天，停一段时间，单位秒


def main():
    # load_RMRB_from_to(datetime(2025, 1, 1), datetime(2025, 1, 2))
    load_RMRB_from_to(datetime(2025,1,1),datetime(2025,5,31))


if __name__ == '__main__':
    main()
