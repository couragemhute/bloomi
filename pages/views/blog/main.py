
from django.views.generic import TemplateView

# Blog View
class BlogTemplateView(TemplateView):
    template_name = 'pages/blog/index.html'

# --- Blog Posts ---
class Post1TemplateView(TemplateView):
    template_name = "pages/blog/post.html"

class Post2TemplateView(TemplateView):
    template_name = "pages/blog/post2.html"

class Post3TemplateView(TemplateView):
    template_name = "pages/blog/post3.html"

class Post4TemplateView(TemplateView):
    template_name = "pages/blog/post4.html"

class Post5TemplateView(TemplateView):
    template_name = "pages/blog/post5.html"

class Post6TemplateView(TemplateView):
    template_name = "pages/blog/post6.html"