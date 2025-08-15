
from django.conf import settings
from django.views.generic import TemplateView

class ProductsTemplateView(TemplateView):
    template_name = 'pages/products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'FB_APP_ID': settings.FB_APP_ID,
            'FB_GRAPH_API_VERSION': settings.FB_GRAPH_API_VERSION,
            'FB_CONFIG_ID': settings.FB_CONFIG_ID,
            'FB_FEATURE_TYPE': settings.FB_FEATURE_TYPE,
        })
        return context
