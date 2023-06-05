from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.TextField(null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    url = models.URLField(null=False, blank=False, unique=True)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
