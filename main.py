import requests 
from bs4 import BeautifulSoup
import re
import json

def get_component(opinion, selector, attribute=None, return_list=False):
    try:
        if attribute:
            return opinion.select(selector).pop(0)[attribute].strip()
        if return_list:
            return [item.get_text().strip() for item in opinion.select(selector)]
        return opinion.select(selector).pop(0).get_text().strip()
    except IndexError:
        return None

selectors = {
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "pros": ["div.review-feature__col:has(> div[class$=\"positives\"]) > div.review-feature__item",
             None,
             True],
    "cons": ["div.review-feature__col:has(> div[class$=\"negatives\"]) > div.review-feature__item",
             None,
             True],
    "verfied": ["div.review-pz"],
    "post_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "usefulness": ["span[id^='votes-yes']"],
    "uselessness": ["span[id^='votes-no']"]
}

all_opinions = []
page = 1
product_id = input("Enter product ID: ")

while True:
    print(page)
    respons = requests.get(f"https://www.ceneo.pl/91715703/opinie-{page}", allow_redirects=False)
    respons = requests.get(f"https://www.ceneo.pl/{product_id}/opinie-{page}", allow_redirects=False)
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
            single_opinion = {key:get_component(opinion,*value)
                              for key, value in selectors.items()}
            single_opinion["opinion_id"] = opinion["data-entry-id"]

            single_opinion["recommendation"] = True if single_opinion[
                "recommendation"] == "Polecam" else False if single_opinion["recommendation"] == "Nie polecam" else None
            single_opinion["stars"] = float(
                single_opinion["stars"].split("/")[0].replace(", ", "."))
            single_opinion["content"] = re.sub(
                "\\s", " ", single_opinion["content"])
            single_opinion["verfied"] = bool(single_opinion["verfied"])
            single_opinion["usefulness"] = int(single_opinion["usefulness"])
            single_opinion["uselessness"] = int(single_opinion["uselessness"])

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

with open(f"./opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, ensure_ascii=False, indent=4)

# print(json.dumps(all_opinions, ensure_ascii=False, indent=4))