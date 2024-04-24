from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """
    TemplateView...
    """
    template_name = "bills/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
