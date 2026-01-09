
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class ChatTemplateView(TemplateView):
    template_name = "chat/index.html"