from django.contrib import admin
from django.urls import path, include
import os

urlpatterns = [
    path(f'{os.environ.get("ADMIN_URL_PATH")}/', admin.site.urls),
    path("api/", include("padfoot_api.urls")),
]
