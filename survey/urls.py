# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.clickjacking import xframe_options_exempt

from survey.views import ConfirmView, IndexView, SurveyCompleted, SurveyDetail
from survey.views.survey_result import serve_result_csv

urlpatterns = [
    url(r"^$", xframe_options_exempt(IndexView.as_view()), name="survey-list"),
    url(r"^confirm/(?P<uuid>\w+)/", xframe_options_exempt(ConfirmView.as_view()), name="survey-confirmation"),
    # url(r"^id/(?P<id>\d+)/", SurveyDetail.as_view(), name="survey-detail"),
    url(r"^csv/(?P<primary_key>\d+)/", serve_result_csv, name="survey-result"),
    url(r"^(?P<slug>\w+)/completed/", xframe_options_exempt(SurveyCompleted.as_view()), name="survey-completed"),
    url(r"^(?P<slug>\w+)-(?P<step>\d+)/", xframe_options_exempt(SurveyDetail.as_view()), name="survey-detail-step"),
    url(r"^(?P<slug>\w+)/", xframe_options_exempt(SurveyDetail.as_view()), name="survey-detail-slug"),
    # path("confirm/<uuid:uuid>", ConfirmView.as_view(), name="survey-confirmation"),
]
