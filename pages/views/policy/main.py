
from django.views.generic import TemplateView

# Blog View
class PolicyTemplateView(TemplateView):
    template_name = 'pages/policy/index.html'
