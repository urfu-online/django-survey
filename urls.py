# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

from django.urls import path, include
from django.contrib import admin
from django.shortcuts import redirect
from django.urls.base import reverse


def home(request):
    """ Permit to not get 404 while testing. """
    return redirect(reverse("survey-list"))


urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("rosetta/", include("rosetta.urls")),
    path("survey/", include("survey.urls")),
    path("embed/", include("survey.urls"), {"emded": True}),
    path("admin/", admin.site.urls),
]
