
from django.views.generic import TemplateView

# Blog View
class CourseTemplateView(TemplateView):
    template_name = 'pages/course/index.html'

# Each course detail page as a simple TemplateView
class Course1TemplateView(TemplateView):
    template_name = "pages/course/course-inner.html"

class Course2TemplateView(TemplateView):
    template_name = "pages/course/course-inner2.html"

class Course3TemplateView(TemplateView):
    template_name = "pages/course/course-inner3.html"

class Course4TemplateView(TemplateView):
    template_name = "pages/course/course-inner4.html"

class Course5TemplateView(TemplateView):
    template_name = "pages/course/course-inner5.html"

class Course6TemplateView(TemplateView):
    template_name = "pages/course/course-inner6.html"
