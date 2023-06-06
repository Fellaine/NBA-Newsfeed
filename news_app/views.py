from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "templates/news_app/article-list.html"
