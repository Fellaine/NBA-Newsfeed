from django.db import IntegrityError
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Article, Source
from .utils import get_espn_news, get_nba_com_news, get_r_nba_news, get_yahoo_news


class ArticleListView(ListView):
    model = Article
    template_name = "templates/news_app/article-list.html"


def scrape_articles(request):
    espn_articles = get_espn_news()
    if espn_articles == 0:
        return HttpResponse("Can't get data")
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
    all_articles = espn_articles + nba_com_articles + yahoo_articles + r_nba_articles

    amount_of_already_saved = 0
    for article in all_articles:
        article_ = Article(
            title=article["title"],
            content=article["content"],
            url=article["url"],
            source_id=article["source_id"],
        )
        try:
            article_.save()
        except IntegrityError:
            amount_of_already_saved -= 1

    return HttpResponse(
        f"Successfully saved {len(all_articles) + amount_of_already_saved} \
        new articles"
    )
