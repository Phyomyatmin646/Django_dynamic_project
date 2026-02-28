from django.urls import path
from .views import Homepage, download_cv
from . import views

urlpatterns = [
    path('', views.Homepage, name='homepage'),
    path('download-cv/', download_cv, name='download_cv'),
]