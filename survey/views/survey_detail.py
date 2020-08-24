# -*- coding: utf-8 -*-
import logging
import urllib

from django.conf import settings
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from survey.decorators import survey_available
from survey.forms import ResponseForm

LOGGER = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class SurveyDetail(View):
    @survey_available
    def get(self, request, *args, **kwargs):

        query_params = urllib.parse.parse_qs(request.GET.urlencode())
        logger.info(query_params)
        if "custom_user" in query_params.keys():
            custom_user = query_params["custom_user"][0]
            query_params["custom_user"] = custom_user
        else:
            custom_user = ""

        survey = kwargs.get("survey")
        step = kwargs.get("step", 0)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.is_all_in_one_page():
                template_name = "survey/one_page_survey.html"
            else:
                template_name = "survey/survey.html"
        if survey.need_logged_user and not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        form = ResponseForm(survey=survey, user=request.user, step=step, custom_user=custom_user)
        logger.warning(kwargs)
        categories = form.current_categories()

        asset_context = {
            # If any of the widgets of the current form has a "date" class, flatpickr will be loaded into the template
            "flatpickr": any([field.widget.attrs.get("class") == "date" for _, field in form.fields.items()])
        }
        context = {
            "response_form": form,
            "survey": survey,
            "categories": categories,
            "step": step,
            "asset_context": asset_context,
            "query_params": urllib.parse.urlencode(query_params),
            "embed": kwargs.get("embed", False),
        }

        return render(request, template_name, context)

    @survey_available
    def post(self, request, *args, **kwargs):
        survey = kwargs.get("survey")
        if survey.need_logged_user and not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        query_params = urllib.parse.parse_qs(request.GET.urlencode())
        if "custom_user" in query_params.keys():
            custom_user = query_params["custom_user"][0]
            query_params["custom_user"] = custom_user
        else:
            custom_user = ""

        form = ResponseForm(
            request.POST, survey=survey, user=request.user, step=kwargs.get("step", 0), custom_user=custom_user
        )
        categories = form.current_categories()

        if not survey.editable_answers and form.response is not None:
            LOGGER.info("Redirects to survey list after trying to edit non editable answer.")
            return redirect(reverse("survey-list"))
        context = {"response_form": form, "survey": survey, "categories": categories}
        if form.is_valid():
            return self.treat_valid_form(form, kwargs, request, survey)
        return self.handle_invalid_form(context, form, request, survey)

    @staticmethod
    def handle_invalid_form(context, form, request, survey):
        LOGGER.info("Non valid form: <%s>", form)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.is_all_in_one_page():
                template_name = "survey/one_page_survey.html"
            else:
                template_name = "survey/survey.html"
        return render(request, template_name, context)

    def treat_valid_form(self, form, kwargs, request, survey):
        session_key = "survey_%s" % (kwargs["slug"],)
        if session_key not in request.session:
            request.session[session_key] = {}
        for key, value in list(form.cleaned_data.items()):
            request.session[session_key][key] = value
            request.session.modified = True
        next_url = form.next_step_url()
        response = None
        query_params = urllib.parse.parse_qs(request.GET.urlencode())
        # logger.info(query_params)
        if "custom_user" in query_params.keys():
            custom_user = query_params["custom_user"][0]
            query_params["custom_user"] = custom_user
        else:
            custom_user = ""

        if survey.is_all_in_one_page():
            response = form.save()
        else:
            # when it's the last step
            if not form.has_next_step():
                save_form = ResponseForm(
                    request.session[session_key], survey=survey, user=request.user, custom_user=custom_user
                )
                if save_form.is_valid():
                    response = save_form.save()
                else:
                    LOGGER.warning("A step of the multipage form failed but should have been discovered before.")
        # if there is a next step
        if next_url is not None:
            return redirect(next_url)
        del request.session[session_key]
        if response is None:
            return redirect(reverse("survey-list"))
        next_ = request.session.get("next", None)
        if next_ is not None:
            if "next" in request.session:
                del request.session["next"]
            return redirect(next_)
        return redirect("survey:survey-confirmation", uuid=response.interview_uuid)
