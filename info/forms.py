"""
forms.py
Формы Django для админки и пользовательских действий.
"""

# info/forms.py
from django import forms
from django.core.validators import FileExtensionValidator
from info.models import News, Document


class ContactForm(forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя"})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите e-mail"})
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "rows": 4, "placeholder": "Ваше сообщение"})
    )


class NewsForm(forms.ModelForm):
    """Форма добавления/редактирования новости"""
    image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg"])],
        widget=forms.FileInput(attrs={"class": "form-control"})
    )
    published_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}),
        label=(
            "Дата и время публикации (оставьте пустым, "
            "чтобы не публиковать сразу)"
        )
    )

    class Meta:
        model = News
        # здесь использовано published_at (как в модели)
        fields = ["title", "content", "image", "published_at"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Введите заголовок"}),
            "content": forms.Textarea(
                attrs={"class": "form-control",
                       "rows": 6, "placeholder": "Текст новости"}),
        }
        labels = {
            "title": "Заголовок",
            "content": "Текст новости",
            "image": "Изображение",
        }


class DocumentForm(forms.ModelForm):
    """Форма загрузки документа"""
    file = forms.FileField(
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "docx", "xls", "xlsx", "txt"])],
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Document
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Название документа"}),
        }
        labels = {
            "title": "Название документа",
            "file": "Файл (PDF, DOCX, XLS, XLSX, TXT)"
        }
