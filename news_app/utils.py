import json
from typing import Literal

import requests
from requests_html import HTMLSession


def get_espn_news(limit: int = 6) -> list[dict] | Literal[0]:
    """
    Get list of espn news with len = limit
    If 404 return 0
    """
    r = requests.get(
        f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news?limit={limit}"  # noqa
    )
    if r.status_code != 200:
        return 0
    request = r.json()
    res = []
    article_ = {}
    for article in request["articles"]:
        article_["title"] = article["headline"]
        article_["content"] = article["description"]
        article_["url"] = article["links"]["web"]["href"]
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
        res.append(article_)

        # TODO : add url

    return res


# pretty = json.dumps(get_espn_news(), indent=4)
# print(pretty)
# print(get_espn_news(10))
# print(get_nba_com_news())
