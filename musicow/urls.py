from django.urls import path

from . import views

urlpatterns = [
    path('', views.MusicCopyrightListView.as_view(), name='music-copyright-list'),
]
