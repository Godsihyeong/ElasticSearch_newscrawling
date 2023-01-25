from bs4 import BeautifulSoup
import requests
import pandas as pd
from elasticsearch import Elasticsearch
from datetime import datetime
import schedule
import time

#### 페이지 url 함수

def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)
    

def makeUrl(search, start_pg, end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(start_page)
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg+1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
            urls.append(url)
            return urls
    


def news_data(row):
    return {
        'title': row['title'],
        'url': row['url'],
        'timestamp': datetime.now()
    }


##### 크롤링 시작 ####

search = ['장바구니+물가', '밥상+물가', '반찬+물가']

## 검색 시작할 페이지 입력
page = 1

## 검색 종료할 페이지 입력
page2 = 5

## naver url 생성



def fun():
    
    search_urls = []
    
    for i in search:
        makeUrl(i, page, page2)
        for j in range(0, len(makeUrl(i, page, page2))):
            search_urls.append(makeUrl(i, page, page2)[j])
            
    headlines = []
    news_urls = []

    for i in search_urls:
        url = requests.get(i)
        html = url.content
        soup = BeautifulSoup(html, 'html.parser')
        titles= soup.select('a.news_tit')
        news_lis = soup.select('section > div > div.group_news > ul > li')
        for j in titles:
            title = j.get_text()
            headlines.append(title)
        for k in news_lis:
            a_href = k.find('a', class_ = 'news_tit')['href']
            news_urls.append(a_href)


    df = pd.DataFrame({'title':headlines, 'url':news_urls})

    es = Elasticsearch(
        cloud_id="Mongta-Dev:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tJGFiMmI0OGJhMzdmYTQxMzdhM2NiMzY4ZGJiMDYyZGE2JDZiMDM2MmM1Y2VkMDQwZDlhMTc3ZjM0YTE3MzhlNWM4",
        basic_auth=('team2_user','team2_user@!uos')
    )
        
    for index, row in df.iterrows():
        doc = news_data(row)
        res = es.index(index = 'news10', document = doc)
        
    print('crawling 하는 중...')
    print(f'{len(headlines)}개의 뉴스 가져옴')
    print('10분 주기로 실행됩니다.')
        
schedule.every(10).seconds.do(fun)

while True:
    schedule.run_pending()
    time.sleep(1)