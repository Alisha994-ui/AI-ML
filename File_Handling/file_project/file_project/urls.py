
from django.contrib import admin
from django.urls import path
from file_app.views import file_upload,uploadpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/upload/", file_upload, name="file_uploading"),
    path('fileupload/',uploadpage,name="uploading")
]
