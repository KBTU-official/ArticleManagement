from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='articles/')

    def __str__(self):
        return self.name