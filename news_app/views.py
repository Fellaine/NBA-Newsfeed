from django.db import IntegrityError
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Article, Source
from .utils import get_espn_news


class ArticleListView(ListView):
    model = Article
    template_name = "templates/news_app/article-list.html"


def scrape_articles(request):
    espn_articles = get_espn_news()
    if espn_articles == 0:
        return HttpResponse("Can't get data from ESPN")
    i = 0
    for article in espn_articles:
        article_ = Article(
            title=article["title"],
            content=article["content"],
            url=article["url"],
            source_id=Source.objects.get(id=1),
        )
        try:
            article_.save()
        except IntegrityError:
            i -= 1

    # TODO add other sources

    return HttpResponse(
        f"Successfully saved {len(espn_articles) + i} new articles from ESPN"
    )
