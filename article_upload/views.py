from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Article
from .forms import ArticleForm


def article_list(request):
    """Display a list of all articles."""
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


def upload_article(request):
    """Handle article upload via a form."""
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'upload_article.html', {'form': form})


def article_detail(request, id):
    """View, edit, and delete an article from a single page."""
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        if "update" in request.POST:
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect(reverse('article_detail', args=[id]))

        elif "delete" in request.POST:
            article.delete()
            return redirect('article_list')

    else:
        form = ArticleForm(instance=article)

    return render(request, 'detail.html', {'article': article, 'form': form})
