from django.views.generic import TemplateView

class AboutTemplateView(TemplateView):
    template_name = 'pages/about/index.html'
