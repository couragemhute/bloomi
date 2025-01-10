
from django.views.generic import TemplateView

# Blog View
class BlogTemplateView(TemplateView):
    template_name = 'pages/blog/index.html'
