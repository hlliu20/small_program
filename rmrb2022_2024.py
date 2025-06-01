# 仅供交流学习
# 爬取人民日报文章保存到.txt文件，图片保存到img文件夹
# 2025.06.01
# V1.0.0

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
base_url =  "https://paper.people.com.cn/rmrb/html"
image_num = 0


def get_title_urls(node_url):
    title_urls = []
    response = requests.get(node_url,headers=headers)
    if response.status_code == 200:
        response.encoding = "utf-8"
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        li_as = soup.select("ul.news-list li a")
        for a in li_as:
            title_urls.append((a.text.strip(), node_url.rsplit("/",1)[0] + "/" + a.get("href")))
    elif response.status_code == 404:
        pass
    else:
        print(f"Failed to retrieve the webpage: {node_url}\nwith response code: {response.status_code}")
    return title_urls

def download_image(url, save_path):
    try:
        # 发送 GET 请求获取图片内容
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功

        # 确保保存路径存在
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存图片到本地文件
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"下载图片时发生错误: {e}")
        return False

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
        if article.find("p"):
            res += "作者/来源：" + article.find("p").text.strip().replace("\r\n          ", " ").replace("\r\n", " ").replace("\xa0", " ") + "\n"
        if article.select("table.pci_c"):
            for pci in article.select("table.pci_c"):
                img_url = "https://paper.people.com.cn/rmrb" + pci.find("img").get("src").split("..")[-1]
                img_path = Path(f"{year}/img/{image_num:06}.{img_url.split('.')[-1]}")
                if download_image(img_url, img_path):
                    res += f"{image_num:06}.{img_url.split('.')[-1]}\n"
                    image_num += 1
                else:
                    res += "图片下载失败\n"
                res += pci.find("p").text.replace("\xa0", " ").replace("\u2002", "  ").replace("\u3000", "  ") + "\n"
        res += "正文：\n"
        for p in article.select("div#ozoom p"):
            res += p.text.replace("\xa0", " ").replace("\u3000", "  ") + "\n"
    else:
        print(f"Failed to retrieve the webpage: {url}\nwith response code: {response.status_code}\n{response.text}")
    return res


def load_RMRB_day(date):
    middle_url = date.strftime("/%Y-%m/%d/")
    # node_num = 20 if is_workday(date) else 8
    file = Path(date.strftime(f"%Y/%Y_%m_%d.txt"))
    res = f"{file}\n"
    if not file.parent.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
    for i in range(1,21):
        node_url = base_url + middle_url + f"nbs.D110000renmrb_{i:02}.htm"
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


def load_RMRB_from_to(date_start, date_end):
    dates = []
    while date_start <= date_end:
        dates.append(date_start)
        date_start += timedelta(days=1)
    for date in tqdm(dates, desc="Processing Dates", unit="date"):
        load_RMRB_day(date)
        time.sleep(5)



def main():
    # load_RMRB_from_to(datetime(2022, 1, 1), datetime(2022, 1, 2))
    load_RMRB_from_to(datetime(2022,1,1),datetime(2024,12,31))


if __name__ == '__main__':
    main()

