import requests
from bs4 import BeautifulSoup
import re
import json

respons = requests.get("https://www.ceneo.pl/91715703#tab=reviews")
all_opinions = []
page = 1

page_dom = BeautifulSoup(respons.text, 'html.parser')
while True:
    print(page)
    respons = requests.get(f"https://www.ceneo.pl/91715703/opinie-{page}", allow_redirects=False)
    if respons.status_code==200:
        page_dom = BeautifulSoup(respons.text, 'html.parser')
        opinions = page_dom.select("div.js_product-review")
        for opinion in opinions:
            opinion_id = opinion["data-entry-id"]
            author = opinion.select("span.user-post__author-name").pop(0).get_text().strip()
            try: 
                recommendation = opinion.select(
                "span.user-post__author-recomendation > em").pop(0).get_text().strip()
                recommendation = True if recommendation=="Polecam" else False
            except IndexError:
                recommendation = None
            stars = opinion.select("span.user-post__score-count").pop(0).get_text().strip()
            stars = float(stars.split("/")[0].replace(",","."))
            content = opinion.select("div.user-post__text").pop(0).get_text().strip()
            content = re.sub("\\s"," ",content)
            pros = opinion.select("div.review-feature__col:has(> div[class$=\"positives\"]) > div.review-feature__item")
            pros = [item.get_text().strip() for item in pros]
            cons = opinion.select("div.review-feature__col:has(> div[class$=\"negatives\"]) > div.review-feature__item")
            cons = [item.get_text().strip() for item in cons]
            try:
                verfied = bool(opinion.select("div.review-pz").pop(0).get_text().strip())
            except IndexError:
                verfied = False
            post_date = opinion.select(
                "span.user-post__published > time:nth-child(1)").pop(0)["datetime"].strip()
            try:
                purchase_date = opinion.select(
                "span.user-post__published > time:nth-child(2)").pop(0)["datetime"].strip()
            except IndexError:
                purchase_date = None
            usefulness = int(opinion.select("span[id^='votes-yes']").pop(0).get_text().strip())
            uselessness = int(opinion.select("span[id^='votes-no']").pop(0).get_text().strip())

opinion = page_dom.select("div.user-post__card").pop(0)
            single_opinion = {
                "opinion_id": opinion_id,
                "author": author,
                "recommendation": recommendation,
                "stars": stars,
                "content": content,
                "pros": pros,
                "cons": cons,
                "verfied": verfied,
                "post_date": post_date,
                "purchase_date": purchase_date,
                "usefulness": usefulness,
                "uselessness": uselessness
            }
            all_opinions.append(single_opinion)
        page += 1
    else: break

opinion_id = opinion["data-entry-id"]
author = opinion.select("span.user-post__author-name").pop(0).get_text().strip()
recommendation = opinion.select(
    "span.user-post__author-recomendation > em").pop(0).get_text().strip()
stars = opinion.select("span.user-post__score-count").pop(0).get_text().strip()
content = opinion.select("div.user-post__text").pop(0).get_text().strip()
pros = opinion.select("div.review-feature__col:has(> div[class$=\"positives\"]) > div.review-feature__item")
pros = [item.get_text().strip() for item in pros]
cons = opinion.select("div.review-feature__col:has(> div[class$=\"negatives\"]) > div.review-feature__item")
cons = [item.get_text().strip() for item in cons]
verfied = opinion.select("div.review-pz").pop(0).get_text().strip()
post_date = opinion.select(
    "span.user-post__published > time:nth-child(1)").pop(0)["datetime"].strip()
purchase_date = opinion.select(
    "span.user-post__published > time:nth-child(2)").pop(0)["datetime"].strip()
usefulness = opinion.select("span[id^='votes-yes']").pop(0).get_text().strip()
uselessness = opinion.select("span[id^='votes-no']").pop(0).get_text().strip()

print(opinion_id, author, recommendation, stars, content, pros, cons, verfied, post_date, purchase_date, usefulness, uselessness, sep="\n")
# print(json.dumps(all_opinions, ensure_ascii=False, indent=4))