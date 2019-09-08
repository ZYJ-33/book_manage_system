import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep

def get(url, params=None, headers=None):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "connection": "close",
    }
    if headers is not None:
        header.update(headers)
    resp = requests.get(url=url, params=params, headers=header)
    return resp


def parse_index(html):
    return set(re.findall('"J_AD_([0-9]*)"', html))

def book_info_iterator(keyword):
    url = 'https://search.jd.com/Search'
    keyword = keyword.encode("gbk")
    params = dict(
        keyword=keyword,
    )
    resp = get(url, params=params)
    ids = parse_index(resp.text)
    for id in ids:
        res = get_detail_page_by_id(id)
        sleep(0.5)
        if res is not None:
            yield res

publisher = re.compile('<a href="//book.jd.com/publish/(.*)_1.html"')
isbn = re.compile('ISBN：([0-9]+)')
version = re.compile('<li title="1">版次：([0-9])</li>')
public_time = re.compile('出版时间：([0-9\-]+)</li>')
regs = [publisher, isbn, version, public_time]

def parsing_paraments(paras):
    res = []
    for reg in regs:
        term = reg.findall(paras)
        if len(term) > 0:
            res.append(term[0])
        else:
            res.append(None)
    return res

def paresing_item_page(html, id):
    '''return [publisher, isbn, version, public_time, author, title, detail] or None'''
    soup = bs(html)
    title = soup.select(".sku-name")
    author = soup.select("#p-author")
    detail = soup.select(".book-detail-content")
    parameter2 = soup.select("#parameter2")
    if len(title) == 0:
        print("no title")
        return None
    else:
        title = title[0].get_text()[2:].strip(" ")
    if len(detail) == 0:
        detail = get_detail_from_cdn(id)
        if detail == None:
            print("no detail")
            return
    else:
        detail = detail[0].get_text()
    if len(author) == 0:
        print("no author")
        author = None
    else:
        author = author[0].get_text()[1:].strip()
    if len(parameter2) == 0:
        print("not para")
        return None
    else:
        res = parsing_paraments(str(parameter2))
    res.append(author)
    res.append(title)
    res.append(detail)
    return res

def get_detail_from_cdn(id):
    resp = get("https://dx.3.cn/desc/{}?cdn=2".format(id))
    text = resp.text.replace("\\n",'')
    soup = bs(text)
    res = soup.select('.book-detail-content')
    if len(res) > 0:
        return res[0].get_text().strip()
    else:
        return None


def get_detail_page_by_id(id):
    url = "https://item.jd.com/{}.html".format(id)
    resp = get(url)
    res = paresing_item_page(resp.text, id)
    return res


# get_jd_index_page_by_keyword("python")

if __name__ == "__main__":
    book_info_iterator("c++")