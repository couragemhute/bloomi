from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Subscriber
from .models import Course, Expert
from .forms import CourseForm, SubscriberForm, ExpertForm
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import  WhatStudentWillLearn
# ---------------- COURSE ----------------
class CourseListView(ListView):
    model = Course
    template_name = "courses/index.html"
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/detail.html"
    context_object_name = "course"


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create.html"
    success_url = reverse_lazy("course_list")


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/update.html"
    success_url = reverse_lazy("course_list")


class CourseDeleteView(DeleteView):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('pk'))

        # Toggle active status instead of deleting
        course.is_active = not course.is_active
        course.save(update_fields=["is_active"])

        status = "activated" if course.is_active else "deactivated"
        messages.success(request, f"{course.title} {status} successfully")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


# ---------------- SUBSCRIBER ----------------
class SubscriberListView(ListView):
    model = Subscriber
    template_name = "subscribers/subscriber_list.html"
    context_object_name = "subscribers"

class SubscriberCreateView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Email cannot be empty.")
            return redirect(request.META.get('HTTP_REFERER'))

        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, "This email is already subscribed.")
            return redirect(request.META.get('HTTP_REFERER'))

        # Save subscriber
        Subscriber.objects.create(email=email)
        messages.success(request, "Thank you for subscribing!")

        return redirect(request.META.get('HTTP_REFERER'))


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = "subscribers/subscriber_confirm_delete.html"
    success_url = reverse_lazy("subscriber_list")


# ---------------- EXPERT ----------------
class ExpertListView(ListView):
    model = Expert
    template_name = "experts/index.html"
    context_object_name = "experts"


class ExpertDetailView(DetailView):
    model = Expert
    template_name = "experts/detail.html"
    context_object_name = "expert"


class ExpertCreateView(CreateView):
    model = Expert
    form_class = ExpertForm
    template_name = "experts/create.html"
    success_url = reverse_lazy("expert_list")


class ExpertUpdateView(UpdateView):
    model = Expert
    form_class = ExpertForm
    template_name = "experts/update.html"
    success_url = reverse_lazy("expert_list")


class ExpertDeleteView(View):
    def post(self, request, *args, **kwargs):
        expert = get_object_or_404(Expert, pk=kwargs.get('pk'))
        expert.delete()
        messages.success(request, f"Expert {expert.user} removed successfully.")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class AddLearningOutcomeView(View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        content = request.POST.get("content")
        if content:
            WhatStudentWillLearn.objects.create(course=course, content=content)
        return redirect(request.META.get("HTTP_REFERER", "/"))
