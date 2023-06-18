from django.db.models import Q
from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "templates/news_app/article-list.html"
    paginate_by = 32
    ordering = ["-id"]

    def get_queryset(self):
        if query := self.request.GET.get("q"):
            object_list = self.model.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by("-id")
        else:
            object_list = self.model.objects.all().order_by("-id")
        return object_list
