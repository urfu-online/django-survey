# -*- coding: utf-8 -*-

import logging

from django.conf.urls import url

from survey.views import ConfirmView, IndexView, SurveyCompleted, SurveyDetail
from survey.views.survey_result import serve_result_csv

logger = logging.getLogger(__name__)

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="survey-list"),
    url(r"^confirm/(?P<uuid>\w+)/", ConfirmView.as_view(), name="survey-confirmation"),
    # url(r"^id/(?P<id>\d+)/", SurveyDetail.as_view(), name="survey-detail"),
    url(r"^csv/(?P<primary_key>\d+)/", serve_result_csv, name="survey-result"),
    url(r"^(?P<slug>\w+)/completed/", SurveyCompleted.as_view(), name="survey-completed"),
    url(r"^(?P<slug>\w+)-(?P<step>\d+)/", SurveyDetail.as_view(), name="survey-detail-step"),
    url(r"^(?P<slug>\w+)/", SurveyDetail.as_view(), name="survey-detail-slug"),
    # path("confirm/<uuid:uuid>", ConfirmView.as_view(), name="survey-confirmation"),
]
