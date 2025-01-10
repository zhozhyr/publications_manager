from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q

from .forms import ProfileEditForm, PublicationForm
from .models import Publication, Issue, Edition, Category

PER_PAGE = 5


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
    current_year = now().strftime('%Y')

    # Пагинация
    page_obj = Paginator(publications, PER_PAGE).get_page(request.GET.get('page'))

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
        'page_obj': page_obj,
    }

    return render(request, "publications/list.html", context)


def publication_detail(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)

    issue = publication.issue
    issue_name = issue.name if issue else "Unknown Issue"

    edition = issue.edition if issue else None
    edition_name = edition.name if edition else "Unknown Edition"

    # Получаем все цитируемые публикации через ManyToMany
    citations = publication.citations.all()

    keywords_list = [keyword.strip() for keyword in publication.keywords.split(',')]

    context = {
        "publication": publication,
        "issue_name": issue_name,
        "edition_name": edition_name,
        "citations": citations,
        'keywords_list': keywords_list,
    }

    return render(request, 'publications/detail.html', context)


class RegisterView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('publications:list')


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)

    # Фильтруем публикации, привязанные к данному пользователю
    publications = Publication.objects.filter(
        issue__date__isnull=False,
        added_by=profile  # Фильтруем по авторству пользователя
    ).select_related('issue__edition', 'issue__edition__category').order_by('-issue__date')

    # Пагинация
    page_obj = Paginator(publications, PER_PAGE).get_page(request.GET.get('page'))

    return render(request, 'publications/profile.html', {
        'profile': profile,
        'page_obj': page_obj
    })


@login_required
def edit_profile(request):
    form = ProfileEditForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("publications:profile", username=request.user.username)

    return render(request, 'publications/user.html', {"form": form})


@login_required
def create_publication(request):
    """
    Представление для создания новой публикации.
    """
    publication_form = PublicationForm()

    if request.method == 'POST':
        publication_form = PublicationForm(request.POST, request.FILES)
        if publication_form.is_valid():
            authors_input = publication_form.cleaned_data['authors']
            authors_list = [username.strip() for username in authors_input.split(',')]

            # Создаём пользователей, если они не существуют
            valid_authors = []

            for username in authors_list:
                user, created = User.objects.get_or_create(username=username)
                valid_authors.append(user.username)

            # Сохраняем публикацию
            publication_instance = publication_form.save(commit=False)
            publication_instance.added_by = request.user  # Сохраняем пользователя, который добавил публикацию
            publication_instance.authors = ', '.join(valid_authors)  # Сохраняем авторов
            publication_instance.save()

            return redirect("publications:profile", username=request.user.username)

    return render(request, "publications/create.html", {"form": publication_form})


@login_required
def edit_publication(request, publication_id):
    """
    Представление для редактирования публикации.
    """
    publication = get_object_or_404(Publication, pk=publication_id)

    # Проверяем, что пользователь — автор публикации
    if request.user != publication.added_by:
        return redirect("publications:publication_detail", publication_id=publication_id)

    if request.method == 'POST':
        publication_form = PublicationForm(request.POST, instance=publication)
        if publication_form.is_valid():
            publication_form.save()
            return redirect("publications:publication_detail", publication_id=publication_id)
    else:
        publication_form = PublicationForm(instance=publication)

    return render(request, "publications/create.html", {"form": publication_form})


@login_required
def delete_publication(request, publication_id):
    """
    Представление для удаления публикации.
    """
    publication = get_object_or_404(Publication, pk=publication_id)

    # Если у публикации есть автор, проверяем права
    if hasattr(publication, 'author') and request.user.pk != publication.author.pk:
        return redirect("publications:detail", publication_id=publication_id)

    publication.delete()
    return redirect("publications:profile", username=request.user.username)
