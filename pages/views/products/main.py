
from django.views.generic import TemplateView

# Blog View
class ProductsTemplateView(TemplateView):
    template_name = 'pages/products/index.html'
