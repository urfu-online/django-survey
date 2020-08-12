# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from survey.models import Survey


class SurveyCompleted(TemplateView):

    template_name = "survey/completed.html"

    def get_context_data(self, **kwargs):
        context = {}
        survey = get_object_or_404(Survey, is_published=True, slug=str(kwargs["slug"]))
        context["survey"] = survey
        return context
