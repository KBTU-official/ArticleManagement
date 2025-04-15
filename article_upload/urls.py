from django.urls import path
from .views import article_list, upload_article, article_detail
from extract_data.views import export_selected_articles 
from . import views

urlpatterns = [
    path('', article_list, name='article_list'),
    path('upload/', upload_article, name='upload_article'),
    path('article_detail/<int:id>/', article_detail, name='article_detail'),
    path("export_selected_articles/", export_selected_articles, name="export_selected_articles")
]