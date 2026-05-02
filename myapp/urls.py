from django.urls import path
from .views import Homepage, download_cv, blog_detail

urlpatterns = [
    path('', Homepage, name='homepage'),
    path('download-cv/', download_cv, name='download_cv'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
]