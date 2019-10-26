from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    This is for rendering out the standings graph
    Some work to be done here
    """
    template_name = "JJE_Standings/standings.html"
