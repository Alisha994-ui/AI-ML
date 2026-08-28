from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    loginpage,
    uploadpage,
    resumespage,
    current_user,
    ResumeViewSet,
    analyze_resumes
)


router = DefaultRouter()

router.register(
    "resumes",
    ResumeViewSet,
    basename="resumes"
)


urlpatterns = [

    # =============================================
    # HTML PAGES
    # =============================================

    path(
        "login/",
        loginpage,
        name="login"
    ),

    path(
        "files/",
        uploadpage,
        name="files"
    ),

    path(
        "resumes/",
        resumespage,
        name="resumes"
    ),


    # =============================================
    # USER API
    # =============================================

    path(
        "api/me/",
        current_user,
        name="current_user"
    ),


    # =============================================
    # JD ANALYSIS API
    # IMPORTANT:
    # YE ROUTER SE PEHLE HONA CHAHIYE
    # =============================================

    path(
        "api/resumes/analyze/",
        analyze_resumes,
        name="analyze-resumes"
    ),


    # =============================================
    # RESUME API
    # =============================================

    path(
        "api/",
        include(router.urls)
    ),

]