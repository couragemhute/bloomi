
from django.conf import settings
from django.views.generic import TemplateView

class ProductsTemplateView(TemplateView):
    template_name = 'pages/products/index.html'
