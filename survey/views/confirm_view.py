# -*- coding: utf-8 -*-

import logging

from django.views.generic import TemplateView

from survey.models import Response

logger = logging.getLogger(__name__)


class ConfirmView(TemplateView):

    template_name = "survey/confirm.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context["uuid"] = str(kwargs["uuid"])
        context["response"] = Response.objects.get(interview_uuid=context["uuid"])
        return context
