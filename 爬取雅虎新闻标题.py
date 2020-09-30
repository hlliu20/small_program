# yahoo.com 爬取雅虎网站新闻标题
import requests
import time
from bs4 import BeautifulSoup

def process_function_2(url):
    """谷歌浏览器，严格一步步找下去"""
    long_str_1 = "stream-item js-stream-content Bgc(t) Pos(r) My(12px) stream-grid-view_Flxb(1/3)"
    long_str_2 = "userintent-hidestrmitem_D(n) Pos(r) D(f) stream-grid-view_Fld(c)"
    re_li = []
    html = requests.get(url).text
    with open('test_html.txt', 'w', encoding="utf-8") as f:
        f.write(html)
    soup = BeautifulSoup(html, 'lxml')
    Masterwrap = soup.find("div", id="Masterwrap")
    Page = Masterwrap.find("div", id="Page")
    Main = Page.find('main', id="Main")
    applet_p_50000314 = Main.find('div', id="applet_p_50000314")
    List_n = applet_p_50000314.find('ul', class_="List(n) P(0) grid-layout stream-items")
    stream_1 = List_n.find_all("li", class_=long_str_1)
    stream_2 = List_n.find_all('li', class_="Fl(start) W(50%)")
    for it in stream_1:
        l1 = it.find('div', class_=long_str_2)
        l2 = l1.find('div', class_="D(f) Fld(c) Fxb(0) Fxg(1)")
        l3 = l2.find('div', class_="Ov(h) Mend(10px)--maw1024")
        h3 = l3.find('h3')
        title = h3.find('a').find('span').text
        print(title)
        re_li.append(title)
    for it in stream_2:
        l1 = it.find('h4').text
        print(l1)
        re_li.append(l1)
    return re_li


def pro_3_simplify(url):
    """上一个的简化版"""
    long_str_1 = "stream-item js-stream-content Bgc(t) Pos(r) My(12px) stream-grid-view_Flxb(1/3)"
    re_li = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    List_n = soup.find('div', id="applet_p_50000314").find('ul')
    stream_1 = List_n.find_all("li", class_=long_str_1)
    stream_2 = List_n.find_all('li', class_="Fl(start) W(50%)")
    for it in stream_1:
        title = it.find('h3').find('a').find('span').text
        print(title)
        re_li.append(title)
    for it in stream_2:
        l1 = it.find('h4').text
        print(l1)
        re_li.append(l1)
    return re_li

def save(title_list):
    """保存新闻标题至txt文件"""
    ti = time.localtime()
    mon, day, hor, mine = ti.tm_mon, ti.tm_mday, ti.tm_hour, ti.tm_min
    file_name_1 = "E:/python_workolace/news_everyday_homework/split/{}_{}_{}_{}.txt".format(mon, day, hor, mine)
    file_name_2 = "E:/python_workolace/news_everyday_homework/news_en_from_09_26.txt"
    title = "{}_{}_{}_{}".format(mon, day, hor, mine)
    row = ""
    with open(file_name_2, "a") as fa:
        fa.write(title + "\n")
        for it in title_list:
            row += it + "\n"
        fa.write(row)
    with open(file_name_1, "w") as f:
        f.write(row)


def main():
    url = "https://www.yahoo.com/"
    title_list = pro_3_simplify(url)
    save(title_list)


if __name__ == "__main__":
    main()
