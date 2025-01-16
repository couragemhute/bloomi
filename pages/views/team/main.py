
from django.views.generic import TemplateView

# Blog View
class TeamTemplateView(TemplateView):
    template_name = 'pages/team/index.html'
