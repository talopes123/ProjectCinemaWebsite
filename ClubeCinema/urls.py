"""ClubeCinema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("ratings/", views.ratings),
    path("profiles/", views.profiles),
    path("profile/<int:id>", views.profile),
    path("login/", views.login),
    path("deleteUser/", views.deleteUser),
    path("deleteMovie/", views.deleteMovie),
    path("deleteRating/", views.deleteRating),
    path("newMovie/", views.newMovie),
    path("logOut/", views.logOut),
    path("signin/", views.signin),
    path("admin/", views.admin),
    path("movies/", views.movies),
    path("movies/<int:id>/rate", views.movieRate),
    path("bigAdmin", admin.site.urls)
]
