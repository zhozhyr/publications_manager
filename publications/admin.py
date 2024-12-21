from django.contrib import admin
from .models import Category, Edition, Issue, Publication


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'edition')
    search_fields = ('name', 'edition__name')
    list_filter = ('edition', 'date')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'issue', 'pages')
    search_fields = ('title', 'authors', 'issue__name', 'keywords')
    list_filter = ('issue', 'authors')
    ordering = ('-issue__date',)
    filter_horizontal = ('citations',)
