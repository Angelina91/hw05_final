from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "about/author.html"


class AboutTechView(TemplateView):
    template_name = "about/tech.html"


class AboutCatView(TemplateView):
    template_name = "about/cat.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
