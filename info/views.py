import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse, FileResponse, Http404

from .models import News, Document, Announcement
from .forms import DocumentForm
from info.utils import get_rss_news


# ------------------------
# Форма для добавления новостей
# ------------------------
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "image"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Заголовок",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Текст новости",
            }),
        }


# ------------------------
# Определяем город по IP
# ------------------------
def get_city_from_ip(request):
    try:
        ip = request.META.get("REMOTE_ADDR", "")
        if ip in ("127.0.0.1", "::1"):
            return "Москва"  # при локальной разработке
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        data = response.json()
        return data.get("city", "Москва")
    except Exception:
        return "Москва"


# ------------------------
# Получаем погоду по API OpenWeather
# ------------------------
def get_weather(city):
    try:
        api_key = "cff5f12ad2a51f76521fa7ab6e74fc48"  # твой ключ
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&units=metric&lang=ru&appid={api_key}"
        )
        response = requests.get(url, timeout=3)
        data = response.json()

        if data.get("main"):
            temp = round(data["main"]["temp"])
            desc = data["weather"][0]["description"].capitalize()
            return f"{city}: {temp}°C, {desc}"
        else:
            return f"Погода в {city}: недоступна"
    except Exception:
        return "Не удалось получить погоду"


# ------------------------
# Главная страница
# ------------------------
def index(request):
    city = request.GET.get("city") or get_city_from_ip(request)
    weather = get_weather(city)
    rss_news = get_rss_news()

    news_list = News.objects.order_by("-published_at", "-created_at")[:3]
    announcements = Announcement.objects.order_by("-date")[:3]
    documents = Document.objects.order_by("-uploaded_at")[:3]

    return render(request, "index.html", {
        "news_list": news_list,
        "announcements": announcements,
        "documents": documents,
        "weather": weather,
        "rss_news": rss_news,
        "city": city,
    })


# ------------------------
# Новости
# ------------------------
def news_list(request):
    news_list = News.objects.order_by("-published_at", "-created_at")
    return render(request, "news_list.html", {"news_list": news_list})


def news_detail(request, pk):
    item = get_object_or_404(News, pk=pk)
    return render(request, "news_detail.html", {"item": item})


# ------------------------
# Документы
# ------------------------
def documents(request):
    documents = Document.objects.all().order_by("-uploaded_at")
    return render(request, "documents.html", {"documents": documents})


def download_document(request, pk):
    """Безопасная отдача файла."""
    doc = get_object_or_404(Document, pk=pk)

    # если файл на внешнем хранилище
    if hasattr(doc.file, "url") and doc.file.url.startswith("http"):
        return redirect(doc.file.url)

    # если файл локально
    file_path = doc.file.path
    if not os.path.exists(file_path):
        raise Http404("Файл не найден")

    return FileResponse(open(file_path, "rb"),
                        as_attachment=True,
                        filename=os.path.basename(file_path))


# ------------------------
# Объявления
# ------------------------
def announcements(request):
    announcements = Announcement.objects.order_by("-date")
    return render(request, "announcements.html",
                  {"announcements": announcements})


# ------------------------
# Добавление документа
# ------------------------
def documents_list(request):
    documents = Document.objects.all()
    form = DocumentForm()

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("documents_list")

    return render(request, "info/documents_list.html", {
        "documents": documents,
        "form": form,
    })


# ------------------------
# Добавление новости
# ------------------------
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("info:index")
    else:
        form = NewsForm()
    return render(request, "add_news.html", {"form": form})


# ------------------------
# Создание суперпользователя (разрешено только если явно включено)
# ------------------------
def create_admin(request):
    allow = os.getenv("ALLOW_CREATE_ADMIN",
                      "False").lower() in ("1", "true", "yes")
    if not allow:
        return HttpResponse("Not allowed", status=403)

    User = get_user_model()
    username = os.getenv("ADMIN_USERNAME", "raul245")
    email = os.getenv("ADMIN_EMAIL", "kirillmendrin245@yandex.com")
    password = os.getenv("ADMIN_PASSWORD", "viper2018")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username,
                                      email=email, password=password)
        return HttpResponse("✅ Суперпользователь создан")
    else:
        return HttpResponse("⚠️ Суперпользователь уже существует")
