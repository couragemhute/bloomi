
from django.views.generic import TemplateView
from course.models import Course
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from course.forms import CourseRatingForm
# Blog View
class CourseTemplateView(TemplateView):
    template_name = 'pages/course/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class CourseDetailTemplateView(DetailView):
    model = Course
    template_name = "pages/course/detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['course_rating_form'] = CourseRatingForm()    
        return context

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
