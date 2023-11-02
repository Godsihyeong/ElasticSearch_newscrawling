# elastic

>ElasticSearch 계정 내용을 담은 py 파일에 '물가'라는 키워드를 네이버에 검색하였을 때 노출되는 상위 50개의 뉴스를 크롤링   
>Elastic애 10분 간격으로 뉴스 데이터가 적재되어 대시보드에 노출되는 뉴스 내용이 달라짐

<h2>News Crawling</h2>

>AWS EC2를 이용하여 매 10분 간격으로 뉴스를 크롤링하는 py파일 생성   
>크롤링된 뉴스는 ElasticSearch에 일정시간 간격으로 적재


