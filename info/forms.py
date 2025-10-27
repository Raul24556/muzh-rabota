"""
forms.py
Формы Django для админки и пользовательских действий.
"""

from django import forms
from django.core.validators import FileExtensionValidator
from info.models import News


class ContactForm(forms.Form):
    """Форма обратной связи (письмо или сообщение)"""
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": "Введите имя"})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control",
                                       "placeholder": "Введите e-mail"})
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={"class": "form-control",
                   "rows": 4, "placeholder": "Ваше сообщение"})
    )


class NewsForm(forms.ModelForm):
    """Форма добавления/редактирования новостей"""
    image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg"])],
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = News
        fields = ["title", "content", "image", "published"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Введите заголовок"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}),
            "published": forms.CheckboxInput(
                attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Заголовок",
            "content": "Текст новости",
            "image": "Изображение",
            "published": "Опубликовать",
        }
