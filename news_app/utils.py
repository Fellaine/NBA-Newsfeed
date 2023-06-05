import json
from typing import Literal

import requests
from requests_html import HTMLSession


def get_espn_news(limit: int = 6) -> list[dict] | Literal[0]:
    """
    Get list of espn news with len = limit.
    If 404 return 0.
    """
    r = requests.get(
        f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news?limit={limit}"  # noqa
    )
    if r.status_code != 200:
        return 0
    response = r.json()
    res = []
    for article in response["articles"]:
        article_ = {
            "title": article["headline"],
            "content": article["description"],
            "url": article["links"]["web"]["href"],
        }
        res.append(article_)
    return res


def get_nba_com_news():
    session = HTMLSession()
    r = session.get("https://www.nba.com/news")
    articles = r.html.find(".ArticleTile_tile__y70gI")
    # print(articles)
    res = []
    # article_ = {}
    for article_el in articles:
        article_ = {}
        article_["title"], article_["content"], _ = article_el.text.split(
            "\n"
        )  # not using timestamp rn
        article_["url"] = article_el.absolute_links.pop()  # get url from set set
        res.append(article_)

    return res


def get_r_nba_news_throttled(limit: int = 6):
    r = requests.get(f"https://www.reddit.com/r/nba/top/.json?count={limit}")
    if r.status_code != 200:
        return 0
    response = r.json()
    res = []
    for post in response["data"]["children"]:
        post_data = post["data"]
        article_ = {
            "title": post_data["title"],
            "content": post_data.get("selftext"),
            "url": post_data["url"],
        }
        if (article_["title"].startswith("[Post Game Thread]")) or (
            article_["title"].startswith("GAME THREAD")
        ):
            article_["content"] = ""
        res.append(article_)

    return res


def get_yahoo_news():
    session = HTMLSession()
    r = session.get("https://sports.yahoo.com/nba/")
    main_article = r.html.find("._ys_13mq8u1")
    main_title, main_content = main_article[0].text.split("\n")
    res = [
        {
            "title": main_title,
            "content": main_content,
            "url": main_article[0].absolute_links.pop(),
        }
    ]
    secondary_articles = r.html.find("._ys_hudz05")
    for article in secondary_articles:
        res.append(
            {
                "title": article.text,
                "content": "",
                "url": article.absolute_links.pop(),
            }
        )
    li_articles = r.html.find(".js-stream-content")
    for article in li_articles:
        article_ = {}
        _, article_["title"], article_["content"] = article.text.split("\n")
        article_["url"] = article.absolute_links.pop()
        res.append(article_)
    return res


def get_r_nba_news():
    session = HTMLSession()
    r = session.get("https://www.reddit.com/r/nba/top/")
    posts = r.html.find("._1poyrkZ7g36PawDueRza-J")
    res = []
    for post in posts:
        title = post.find("h3")[0].text
        content = ""
        if not (title.startswith("[Post Game Thread]")) and not (
            title.startswith("GAME THREAD")
        ):
            for paragraph in post.find("p"):
                content += paragraph.text + r"\n"
        url = post.find(".SQnoC3ObvgnGjWt90zD9Z")[0].absolute_links.pop()
        res.append(
            {
                "title": title,
                "content": content,
                "url": url,
            }
        )
    return res


# print("ESPN NEWS: ")
# print(json.dumps(get_espn_news(), indent=4))
# print("NBA.COM NEWS: ")
# print(json.dumps(get_nba_com_news(), indent=4))
# # print("r/NBA NEWS: ")
# # print(json.dumps(get_r_nba_news_throttled(), indent=4))
# print("YAHOO NEWS: ")
# print(json.dumps(get_yahoo_news(), indent=4))
# print("r/NBA NEWS: ")
# print(json.dumps(get_r_nba_news(), indent=4))
