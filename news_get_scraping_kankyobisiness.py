import requests
from bs4 import BeautifulSoup
import csv
import datetime

# 環境ビジネスの太陽光発電関連記事URLを読み込み
url = "https://www.kankyo-business.jp/solar/news"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# 保存するcsvのパス、今日の日付を名前に追加する
dt_now = datetime.datetime.now()
csv_path = "環境ビジネス" + dt_now.strftime('%Y年%m月%d日') + ".csv"
print(csv_path)

# divタグのクラスを指定して、ニュースそれぞれのURLとタイトルを取得し、リスト化
elems = soup.find("div", class_ = "p-index__single p-index__news")
elems_news = elems.find_all("a")
url_news_list = []
title_list = []
for elem_news in elems_news:
    url_news_list.append(elem_news.get("href"))
    title_list.append(elem_news.get_text(strip=True))

# csvを開いて、書き込み
with open(csv_path, 'w', newline='', encoding='utf_8_sig') as file:
    writer = csv.writer(file)
    writer.writerow(["No.", "Title", "Text"])

    # ニュースそれぞれに介してニュース本文を取得
    for i in range(len(url_news_list)):
        r_2 = requests.get(url_news_list[i])
        soup_2 = BeautifulSoup(r_2.text, "html.parser")
        elems_2 = soup_2.find("div", class_ = "p-post__body")
        elems_news_2 = elems_2.find_all("p")
        news_text = ""
        for elem_news_2 in elems_news_2:
            news_text += elem_news_2.get_text(strip=True)
        writer.writerow([i+1, title_list[i], news_text])