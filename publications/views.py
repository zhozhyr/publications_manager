from datetime import datetime

from django.http import Http404
from django.shortcuts import render, redirect
from .data_store import *

new_publications = {publication['id']: publication for publication in publications}


def list_publications(request):
    # Получение фильтров из GET-запроса
    author_filter = request.GET.get("author", "").strip()
    edition_filter = request.GET.get("edition", "").strip()
    issue_filter = request.GET.get("issue", "").strip()
    category_filter = request.GET.get("category", "").strip()

    # Фильтрация публикаций
    filtered_publications = publications

    if author_filter:
        filtered_publications = [
            pub for pub in filtered_publications if author_filter in pub["authors"]
        ]
    if issue_filter:
        filtered_publications = [
            pub for pub in filtered_publications if str(pub["issue_id"]) == issue_filter
        ]
    if edition_filter:
        filtered_publications = [
            pub
            for pub in filtered_publications
            if str(next(
                (issue["edition_id"] for issue in issues if issue["id"] == pub["issue_id"]),
                None,
            )) == edition_filter
        ]
    if category_filter:
        filtered_publications = [
            pub
            for pub in filtered_publications
            if str(next(
                (edition["category_id"]
                 for edition in editions
                 if edition["id"] == next(
                    (issue["edition_id"] for issue in issues if issue["id"] == pub["issue_id"]),
                    None,
                )),
                None,
            )) == category_filter
        ]
    current_year = datetime.now().strftime('%Y')
    context = {
        "publications": filtered_publications,
        "authors": {author for pub in publications for author in pub["authors"]},
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
    if publication_id not in new_publications:
        raise Http404(f'Publication {publication_id} not found')

    publication = new_publications[publication_id]

    issue = next((issue for issue in issues if issue['id'] == publication['issue_id']), None)
    issue_name = issue['name'] if issue else "Unknown Issue"

    edition = next((edition for edition in editions if edition['id'] == issue['edition_id']), None) if issue else None
    edition_name = edition['name'] if edition else "Unknown Edition"

    citated = []
    for cited_id in publication.get('citations', []):
        cited_publication = new_publications.get(cited_id)
        if cited_publication:
            citated.append({
                "id": cited_id,
                "title": cited_publication['title'],
                "authors": cited_publication['authors']
            })

    context = {
        "publication": publication,
        "issue_name": issue_name,
        "edition_name": edition_name,
        "citated": citated,
    }

    return render(request, 'publications/detail.html', context)
