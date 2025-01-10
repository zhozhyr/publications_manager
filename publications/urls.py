from django.urls import path
from . import views

app_name = "publications"

urlpatterns = [
    path("", views.list_publications, name="list"),
    path('publications/<int:publication_id>/', views.publication_detail, name='publication_detail'),

    # Публикации: создание, редактирование и удаление
    path('publications/create/', views.create_publication, name='create_publication'),
    path('publications/<int:publication_id>/edit/', views.edit_publication, name='edit_publication'),
    path('publications/<int:publication_id>/delete/', views.delete_publication, name='delete_publication'),

    # Профиль пользователя
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
