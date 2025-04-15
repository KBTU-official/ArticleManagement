from django.urls import path
from . import views
from .views import process_articles



urlpatterns = [
    path("process/<int:article_id>/", views.process_articles, name="process_articles"),
    path("article/<int:article_id>/", views.view_article, name="view_article"),
    path("export/<int:article_id>/", views.export_to_excel, name="export_to_excel"),

]
