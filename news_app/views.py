from django.db import IntegrityError
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Article
from .utils import get_all_articles


class ArticleListView(ListView):
    model = Article
    template_name = "templates/news_app/article-list.html"


def scrape_articles(request):
    all_articles = get_all_articles()
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
