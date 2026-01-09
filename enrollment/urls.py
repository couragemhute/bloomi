from django.test import TestCase

# Create your tests here.
from django.urls import path

from enrollment.views import *

urlpatterns = [
    path(
        "enrollments/",
        CourseEnrollmentListView.as_view(),
        name="course_enrollment_list"
    ),

    path(
        "enrollments/create/",
        CourseEnrollmentCreateView.as_view(),
        name="course_enrollment_create"
    ),

    path(
        "enrollments/<int:pk>/",
        CourseEnrollmentDetailView.as_view(),
        name="course_enrollment_detail"
    ),

    path(
        "enrollments/<int:pk>/update/",
        CourseEnrollmentUpdateView.as_view(),
        name="course_enrollment_update"
    ),

    path(
        "enrollments/<int:pk>/delete/",
        CourseEnrollmentDeleteView.as_view(),
        name="course_enrollment_delete"
    ),

    path(
    "courses/<int:pk>/enroll/",
    CourseEnrollModalView.as_view(),
    name="course_enroll_modal"
)

]
