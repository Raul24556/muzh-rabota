from django.db import models
from django.core.exceptions import ValidationError
import os


class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание")
    image = models.ImageField("Изображение", upload_to='news_images/',
                              blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    published_at = models.DateTimeField("Дата публикации",
                                        null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    date = models.DateField("Дата")
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to='announcement_images/',
                              blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField("Название документа", max_length=255)
    file = models.FileField("Файл", upload_to='documents/')
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def clean(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext not in ['.pdf', '.docx']:
            raise ValidationError('Допустимые форматы: PDF и DOCX')

    def __str__(self):
        return self.title
