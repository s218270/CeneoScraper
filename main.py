import requests
from bs4 import BeautifulSoup

respons = requests.get("https://www.ceneo.pl/91715703#tab=reviews")

page_dom = BeautifulSoup(respons.text, 'html.parser')

opinion = page_dom.select("div.user-post__card").pop(0)

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
