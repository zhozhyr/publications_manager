from django.urls import path
from . import views

app_name = "publications"

urlpatterns = [
    path("", views.list_publications, name="list"),
    path('publications/<int:publication_id>/', views.publication_detail, name='publication_detail'),
]
