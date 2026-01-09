from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from role.mixins.role_permission_required import RolePermissionRequiredMixin
from enrollment.models import CourseEnrollment
from enrollment.forms import CourseEnrollmentForm
from course.models import Course


class CourseEnrollmentListView(LoginRequiredMixin, RolePermissionRequiredMixin, ListView):
    model = CourseEnrollment
    context_object_name = "enrollments"
    template_name = "course_enrollment/index.html"

    def get_required_permissions(self):
        return ["view_courseenrollment"]

class CourseEnrollmentCreateView(
    LoginRequiredMixin,
    RolePermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = CourseEnrollment
    form_class = CourseEnrollmentForm
    template_name = "course_enrollment/create.html"
    success_message = "Student enrolled successfully"

    def get_success_url(self):
        return reverse("course_enrollment_list")

    def get_required_permissions(self):
        return ["add_courseenrollment"]


class CourseEnrollmentUpdateView(
    LoginRequiredMixin,
    RolePermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = CourseEnrollment
    form_class = CourseEnrollmentForm
    template_name = "course_enrollment/update.html"
    success_message = "Enrollment updated successfully"

    def get_success_url(self):
        return reverse("course_enrollment_list")

    def get_required_permissions(self):
        return ["change_courseenrollment"]


class CourseEnrollmentDetailView(
    LoginRequiredMixin,
    RolePermissionRequiredMixin,
    DetailView
):
    model = CourseEnrollment
    context_object_name = "enrollment"
    template_name = "course_enrollment/detail.html"

    def get_required_permissions(self):
        return ["view_courseenrollment"]


class CourseEnrollmentDeleteView(
    LoginRequiredMixin,
    RolePermissionRequiredMixin,
    SuccessMessageMixin,
    View
):
    def get(self, request, **kwargs):
        enrollment = get_object_or_404(CourseEnrollment, pk=kwargs.get("pk"))
        enrollment.delete()
        messages.success(request, "Enrollment removed successfully")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    def get_required_permissions(self):
        return ["delete_courseenrollment"]


class CourseEnrollModalView(
    LoginRequiredMixin,
    RolePermissionRequiredMixin,
    View
):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get("pk"))
        student = request.user

        # ✅ Prevent double enrollment
        if CourseEnrollment.objects.filter(
            course=course,
            student=student
        ).exists():
            messages.warning(request, "You are already enrolled in this course.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        # ✅ Enroll student
        CourseEnrollment.objects.create(
            course=course,
            student=student
        )

        messages.success(request, "You have successfully enrolled in this course.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_required_permissions(self):
        return ["add_courseenrollment"]
