from typing import Any, Literal

import requests
from requests_html import HTMLSession

from .models import Source


def get_espn_news(limit: int = 6) -> list[dict] | Literal[0]:
    """Get nba articles from espn.com

    Args:
        limit (int, optional): maximum number of articles to retrieve. Defaults to 6.

    Returns:
        list[dict] | Literal[0]: each dict contains article's title, content, and URL.
        If error returns 0
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


def get_nba_com_news() -> list[dict]:
    """Scrape news articles from nba.com

    Returns:
        list[dict]: each dict contains single article's title, content, and URL.
    """
    session = HTMLSession()
    r = session.get("https://www.nba.com/news")
    articles = r.html.find(".ArticleTile_tile__y70gI")
    res = []
    for article_el in articles:
        article_ = {}
        article_["title"], article_["content"], _ = article_el.text.split(
            "\n"
        )  # not using timestamp rn
        article_["url"] = article_el.absolute_links.pop()  # get url from set of links
        res.append(article_)

    return res


def get_r_nba_news_throttled(limit: int = 6) -> list[dict] | Literal[0]:
    """Get articles from nba subreddit

    Args:
        limit (int, optional): number of articles to retrieve. Defaults to 6.

    Returns:
        list[dict] | Literal[0]: each dict contains article's title, content, and URL.
        If error returns 0
    """
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


def get_yahoo_news() -> list[dict]:
    """Scrape news articles from nba.com

    Returns:
        list[dict]: each dict contains single article's title, content, and URL.
    """
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


def get_r_nba_news() -> list[dict]:
    """Scrape posts from nba subreddit

    Returns:
        list[dict]: each dict contains single posts's title, content, and URL.
    """
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


def get_all_articles() -> list[dict] | list[Any]:
    """Unify articles from all sources

    Returns:
        list[dict] | list[Any]: all articles from all sources
        with their titles, contents, and URLs.
        If error returns empty list
    """
    espn_articles = get_espn_news()
    if espn_articles == 0:
        return []
    espn_source = Source.objects.get(id=1)
    for article in espn_articles:
        article["source_id"] = espn_source

    nba_com_articles = get_nba_com_news()
    nba_com_source = Source.objects.get(id=2)
    for article in nba_com_articles:
        article["source_id"] = nba_com_source

    yahoo_articles = get_yahoo_news()
    yahoo_source = Source.objects.get(id=3)
    for article in yahoo_articles:
        article["source_id"] = yahoo_source

    r_nba_articles = get_r_nba_news()
    r_nba_source = Source.objects.get(id=4)
    for article in r_nba_articles:
        article["content"] = article["content"].replace("\\n", " ")
        article["source_id"] = r_nba_source
    return espn_articles + nba_com_articles + yahoo_articles + r_nba_articles
