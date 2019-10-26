from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse


class IndexView(TemplateView):
    template_name = "JJE_Main/index.html"

    def get(self, request, *args, **kwargs):
        return redirect(reverse('waivers_index'))
