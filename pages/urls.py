from django.urls import path
from .views import AboutTemplateView, ServicesTemplateView, BlogTemplateView, ContactTemplateView, ProductsTemplateView, TeamTemplateView

urlpatterns = [
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('services/', ServicesTemplateView.as_view(), name='services'),
    path('blog/', BlogTemplateView.as_view(), name='blog'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('products/', ProductsTemplateView.as_view(), name='products'),
    path('team/', TeamTemplateView.as_view(), name='team'),
]
