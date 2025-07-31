
from django.views.generic import TemplateView

# Blog View
class TermsAndConditionsTemplateView(TemplateView):
    template_name = 'pages/terms_and_conditions/index.html'
