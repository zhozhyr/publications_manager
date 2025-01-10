from django.db import models
from django.contrib.auth import get_user_model

# Получение модели User
User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Введите название"
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Edition(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='editions',
        verbose_name="Категория",
        help_text="Выберите категорию, к которой относится это издание"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Издание"
        verbose_name_plural = "Издания"


class Issue(BaseModel):
    date = models.DateField(
        verbose_name="Дата выпуска",
        help_text="Укажите дату выпуска"
    )
    edition = models.ForeignKey(
        Edition,
        on_delete=models.CASCADE,
        related_name='issues',
        verbose_name="Издание",
        help_text="Выберите издание, к которому относится этот выпуск"
    )

    def __str__(self):
        return f"{self.name} ({self.edition.name})"

    class Meta:
        verbose_name = "Выпуск"
        verbose_name_plural = "Выпуски"


class Publication(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название публикации",
        help_text="Введите название публикации"
    )
    authors = models.TextField(
        verbose_name="Авторы",
        help_text="Укажите авторов публикации, разделяя их запятой"
    )
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_publications')
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name="Выпуск",
        help_text="Выберите выпуск, к которому относится эта публикация"
    )
    pages = models.CharField(
        max_length=20,
        verbose_name="Страницы",
        help_text="Укажите страницы, на которых опубликована статья"
    )
    keywords = models.TextField(
        verbose_name="Ключевые слова",
        help_text="Введите ключевые слова, разделяя их запятой"
    )
    abstract = models.TextField(
        verbose_name="Аннотация",
        help_text="Введите аннотацию публикации"
    )
    citations = models.ManyToManyField(
        'self',
        blank=True,
        related_name='cited_by',
        symmetrical=False,
        verbose_name="Цитаты",
        help_text="Выберите публикации, которые ссылаются на эту статью"
    )
    text = models.TextField(
        verbose_name="Текст публикации",
        help_text="Введите полный текст публикации"
    )
    file = models.FileField(
        null=True,
        blank=True,
        verbose_name="Файл публикации",
        help_text="Загрузите файл публикации"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
