from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput, Textarea
from .models import Publication


class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'authors', 'issue', 'pages', 'keywords', 'abstract', 'citations', 'text', 'file']
        widgets = {
            'authors': Textarea(attrs={
                'rows': 1,
                'placeholder': 'Введите имена авторов через запятую. Например: Иванов И.И., Иванов И.И.'
            }),
            'keywords': Textarea(attrs={'rows': 3, 'placeholder': 'Введите ключевые слова, разделяя их запятой'}),
            'abstract': Textarea(attrs={'rows': 5, 'placeholder': 'Введите аннотацию публикации'}),
            'text': Textarea(attrs={'rows': 10, 'placeholder': 'Вставьте введение статьи'}),
        }


class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
