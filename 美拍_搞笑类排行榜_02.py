import requests
from bs4 import BeautifulSoup
import csv


def process():
    url = 'https://www.meipai.com/rank/13'
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    vedio_list = soup.find_all('li', class_="feed-item pr")
    re_li = []
    for it in vedio_list:
        author = it.find('a', itemprop="author").text.strip()
        datetime = it.find('span', class_="feed-time pa").text.strip()
        try:
            title = it.find('h1').text.strip()
        except AttributeError:
            title = it.find('a', itemprop="description").text.strip()
        vedio_link = "https://www.meipai.com" + it.find('a', itemprop="description").get('href')
        like = it.find('span', class_="pr top-2").text
        comments = it.find('span', class_="pr top-3").text
        re_li.append([title, datetime, author, vedio_link, like, comments])
    return re_li


def main():
    Top20 = process()
    with open("Top20.csv", 'w', newline='', encoding='utf-8')as f:
        pen = csv.writer(f)
        pen.writerow(['标题', '时间', '作者', '网址', '点赞', '评论'])
        for it in Top20:
            pen.writerow(it)


if __name__ == "__main__":
    main()