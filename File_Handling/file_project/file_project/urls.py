from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from file_app.views import ResumeViewSet, uploadpage

router = DefaultRouter()
router.register(r"resumes", ResumeViewSet, basename="resume")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", uploadpage, name="uploadpage"),
    path("api/", include(router.urls)),
]
