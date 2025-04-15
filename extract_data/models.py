from django.db import models


class ArticleData(models.Model):
    title = models.CharField(max_length=10000)
    abstract = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    journal_name = models.CharField(max_length=5000, blank=True, null=True)
    authors = models.TextField(blank=True, null=True)
    article_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
