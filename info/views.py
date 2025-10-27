from django.shortcuts import render, get_object_or_404
from .models import News, Document, Announcement


def index(request):
    news_list = News.objects.order_by('-created_at')[:3]
    announcements = Announcement.objects.order_by('-date')[:3]
    documents = Document.objects.order_by('-uploaded_at')[:3]
    return render(request, 'index.html', {
        'news_list': news_list,
        'announcements': announcements,
        'documents': documents,
    })


def news_list(request):
    news_list = News.objects.order_by('-created_at')
    return render(request, 'news_list.html', {'news_list': news_list})


def news_detail(request, pk):
    item = get_object_or_404(News, pk=pk)
    return render(request, "news_detail.html", {"item": item})


def documents(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, "documents.html", {"documents": documents})


def announcements(request):
    announcements = Announcement.objects.order_by('-date')
    return render(request, "announcements.html",
                  {"announcements": announcements})
