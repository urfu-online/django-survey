# -*- coding: utf-8 -*-

from django.urls import path
from django.views.decorators.clickjacking import xframe_options_exempt

from survey.views import ConfirmView, IndexView, SurveyCompleted, SurveyDetail
from survey.views.survey_result import serve_result_csv

app_name = 'survey'

urlpatterns = [
    path("", xframe_options_exempt(IndexView.as_view()), name="survey-list"),
    path("confirm/<uuid:uuid>/", xframe_options_exempt(ConfirmView.as_view()), name="survey-confirmation"),
    path("csv/<int:primary_key>/", serve_result_csv, name="survey-result"),
    path("<slug:slug>/completed/", xframe_options_exempt(SurveyCompleted.as_view()), name="survey-completed"),
    path("<slug:slug>-<int:step>/", xframe_options_exempt(SurveyDetail.as_view()), name="survey-detail-step"),
    path("<slug:slug>/", xframe_options_exempt(SurveyDetail.as_view()), name="survey-detail-slug"),
]
