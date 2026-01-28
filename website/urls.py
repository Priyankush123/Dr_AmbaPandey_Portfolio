from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from core.models import Paper

def home(request):
    books = Paper.objects.filter(category="book")
    publications = Paper.objects.filter(category="publication")

    return render(
        request,
        "index.html",
        {
            "books": books,
            "publications": publications,
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
