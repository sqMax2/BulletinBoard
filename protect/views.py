from django.shortcuts import render
import pytz
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView


class IndexView(LoginRequiredMixin, FormView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context
