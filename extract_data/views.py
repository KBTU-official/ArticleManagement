from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ArticleData
from article_upload.models import Article
from .utils import extract_article_info
import pandas as pd

def process_articles(request, article_id):
    """Extract article information and save it in the database."""
    try:
        article = get_object_or_404(Article, id=article_id)
        extracted_data = extract_article_info(article.file.path)

        article_data, created = ArticleData.objects.update_or_create(
            title=extracted_data["title"],
            defaults={
                "abstract": extracted_data["abstract"],
                "year": extracted_data["year"],
                "country": extracted_data["country"],
                "journal_name": extracted_data["journal_name"],
                "authors": extracted_data["authors"],
                "article_link": extracted_data["article_link"],
            }
        )
        return redirect("view_article", article_id=article_data.id)

    except Article.DoesNotExist:
        return HttpResponse("Article not found", status=404)

def view_article(request, article_id):
    """Display and allow modification of extracted article details."""
    article = get_object_or_404(ArticleData, id=article_id)

    if request.method == "POST":
        article.title = request.POST.get("title")
        article.abstract = request.POST.get("abstract")
        article.year = request.POST.get("year")
        article.country = request.POST.get("country")
        article.journal_name = request.POST.get("journal_name")
        article.authors = request.POST.get("authors")
        article.article_link = request.POST.get("article_link")
        article.save()
        return redirect("view_article", article_id=article.id)

    return render(request, "article_detail.html", {"article": article})

def export_to_excel(request, article_id):
    """Export a single article's details to an Excel file."""
    article = get_object_or_404(ArticleData, id=article_id)

    data = {
        "Title": [article.title],
        "Abstract": [article.abstract],
        "Year": [article.year],
        "Country": [article.country],
        "Journal": [article.journal_name],
        "Authors": [article.authors],
        "Article Link": [article.article_link],
    }

    df = pd.DataFrame(data)
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{article.title}.xlsx"'
    df.to_excel(response, index=False)

    return response

def export_selected_articles(request):
    """Export selected articles' details to an Excel file."""
    if request.method == "POST":
        selected_article_ids = request.POST.getlist("selected_articles")
        if not selected_article_ids:
            return HttpResponse("No articles selected", status=400)

        extracted_data_list = []
        for article_id in selected_article_ids:
            article = get_object_or_404(Article, id=article_id)
            extracted_data = extract_article_info(article.file.path)

            extracted_data_list.append({
                "Title": extracted_data.get("title", ""),
                "Abstract": extracted_data.get("abstract", ""),
                "Year": extracted_data.get("year", ""),
                "Country": extracted_data.get("country", ""),
                "Journal": extracted_data.get("journal_name", ""),
                "Authors": extracted_data.get("authors", ""),
                "Article Link": extracted_data.get("article_link", ""),
            })

        df = pd.DataFrame(extracted_data_list)
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="Extracted_Articles.xlsx"'
        df.to_excel(response, index=False)

        return response

    return HttpResponse("Invalid request", status=400)
