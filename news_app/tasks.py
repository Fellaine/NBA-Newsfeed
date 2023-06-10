from django.db import IntegrityError
from django.db.utils import DataError

from nbanews.celery import app

from .models import Article
from .utils import get_all_articles


@app.task
def scrape_articles():
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
        except (IntegrityError, DataError):
            amount_of_already_saved -= 1
    return (
        f"Successfully saved {len(all_articles) + amount_of_already_saved} new articles"
    )
