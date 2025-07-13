import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Config
from .nabguinead import NabGuinead


class SettingsView(TemplateView):
    template_name = "nabguinead/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config"] = Config.load()
        return context

    def post(self, request, *args, **kwargs):
        config = Config.load()
        config.guinea_frequency = int(request.POST["guinea_frequency"])
        config.save()
        NabGuinead.signal_daemon()
        context = super().get_context_data(**kwargs)
        context["config"] = config
        return render(request, SettingsView.template_name, context=context)

    def put(self, request, *args, **kwargs):
        config = Config.load()
        config.next_guinea = datetime.datetime.now(datetime.timezone.utc)
        config.save()
        NabGuinead.signal_daemon()
        return JsonResponse({"status": "ok"})


class RFIDDataView(TemplateView):
    template_name = "nabguinead/rfid-data.html"

    def get(self, request, *args, **kwargs):
        """
        Unserialize RFID application data
        """
        return render(request, RFIDDataView.template_name)

    def post(self, request, *args, **kwargs):
        """
        Serialize RFID application data
        """
        return JsonResponse({"data": ""})
