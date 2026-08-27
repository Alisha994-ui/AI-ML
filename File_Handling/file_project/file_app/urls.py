from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    loginpage,
    uploadpage,
    resumespage,
    current_user,
    ResumeViewSet
)

router = DefaultRouter()
router.register("resumes", ResumeViewSet, basename="resumes")

urlpatterns = [
    path("login/", loginpage, name="login"),
    path("files/", uploadpage, name="files"),
    path("resumes/", resumespage, name="resumes"),
    path("api/me/", current_user, name="current_user"),
    path("api/", include(router.urls)),
]