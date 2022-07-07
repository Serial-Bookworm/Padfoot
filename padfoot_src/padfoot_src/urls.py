from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('itisme/', admin.site.urls),
    path("api/", include("padfoot_api.urls")),
]
