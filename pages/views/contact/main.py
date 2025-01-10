
from django.views.generic import TemplateView

# Contact View
class ContactTemplateView(TemplateView):
    template_name = 'pages/contact/index.html'
