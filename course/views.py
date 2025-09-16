from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Subscriber
from .models import Course, Expert
from .forms import CourseForm, SubscriberForm, ExpertForm


# ---------------- COURSE ----------------
class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("course_list")


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("course_list")


class CourseDeleteView(DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    success_url = reverse_lazy("course_list")


# ---------------- SUBSCRIBER ----------------
class SubscriberListView(ListView):
    model = Subscriber
    template_name = "subscribers/subscriber_list.html"
    context_object_name = "subscribers"


class SubscriberCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = "subscribers/subscriber_form.html"
    success_url = reverse_lazy("subscriber_list")


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = "subscribers/subscriber_confirm_delete.html"
    success_url = reverse_lazy("subscriber_list")


# ---------------- EXPERT ----------------
class ExpertListView(ListView):
    model = Expert
    template_name = "experts/expert_list.html"
    context_object_name = "experts"


class ExpertDetailView(DetailView):
    model = Expert
    template_name = "experts/expert_detail.html"
    context_object_name = "expert"


class ExpertCreateView(CreateView):
    model = Expert
    form_class = ExpertForm
    template_name = "experts/expert_form.html"
    success_url = reverse_lazy("expert_list")


class ExpertUpdateView(UpdateView):
    model = Expert
    form_class = ExpertForm
    template_name = "experts/expert_form.html"
    success_url = reverse_lazy("expert_list")


class ExpertDeleteView(DeleteView):
    model = Expert
    template_name = "experts/expert_confirm_delete.html"
    success_url = reverse_lazy("expert_list")
