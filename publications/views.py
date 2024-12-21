from datetime import datetime

from django.http import Http404
from django.shortcuts import render
from .models import Publication, Issue, Edition, Category


def list_publications(request):
    # Получение фильтров из GET-запроса
    author_filter = request.GET.get("author", "").strip()
    edition_filter = request.GET.get("edition", "").strip()
    issue_filter = request.GET.get("issue", "").strip()
    category_filter = request.GET.get("category", "").strip()

    # Фильтрация публикаций
    publications = Publication.objects.all()

    if author_filter:
        publications = publications.filter(authors__icontains=author_filter)
    if issue_filter:
        publications = publications.filter(issue__id=issue_filter)
    if edition_filter:
        publications = publications.filter(issue__edition__id=edition_filter)
    if category_filter:
        publications = publications.filter(issue__edition__category__id=category_filter)

    # Получаем все необходимые данные для отображения
    authors = Publication.objects.values_list('authors', flat=True).distinct()
    editions = Edition.objects.all()
    issues = Issue.objects.all()
    categories = Category.objects.all()
    current_year = datetime.now().strftime('%Y')

    context = {
        "publications": publications,
        "authors": authors,
        "editions": editions,
        "issues": issues,
        "categories": categories,
        "selected_filters": {
            "author": author_filter,
            "edition": edition_filter,
            "issue": issue_filter,
            "category": category_filter,
        },
        "current_year": current_year,
    }

    return render(request, "publications/list.html", context)


def publication_detail(request, publication_id):
    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        raise Http404(f'Publication {publication_id} not found')

    issue = publication.issue
    issue_name = issue.name if issue else "Unknown Issue"

    edition = issue.edition if issue else None
    edition_name = edition.name if edition else "Unknown Edition"

    # Получаем все цитируемые публикации через ManyToMany
    citations = publication.citations.all()  # Это уже не строка, а QuerySet

    keywords_list = [keyword.strip() for keyword in publication.keywords.split(',')]

    context = {
        "publication": publication,
        "issue_name": issue_name,
        "edition_name": edition_name,
        "citations": citations,
        'keywords_list': keywords_list,
    }

    return render(request, 'publications/detail.html', context)

