from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from course.forms import CourseRatingForm
from course.models import CourseRating


class CourseRatingListView(LoginRequiredMixin, ListView):
    model = CourseRating
    context_object_name = "course_rating"
    template_name = "pages/course/course_rating/list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseRatingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CourseRating
    form_class = CourseRatingForm
    template_name = "pages/course/course_rating/create.html"
    success_message = "Product rating created successfully"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


class CourseRatingDetailsView(LoginRequiredMixin, DetailView):
    model = CourseRating
    context_object_name = "course_rating"
    template_name = "pages/course/course_rating/details.html"


class CourseRatingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CourseRating
    context_object_name = "course_rating"
    template_name = "pages/course/course_rating/update.html"
    form_class = CourseRatingForm
    success_message = "Product rating updated successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')



class CourseRatingDeleteView(View):
    def get(self, request, **kwargs):
        rating = get_object_or_404(CourseRating, pk=kwargs.get('pk'))
        rating.delete()
        messages.success(request, f'{rating} deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))