from django import forms
from blog.forms import StyledModelForm
from enrollment.models import CourseEnrollment


class CourseEnrollmentForm(StyledModelForm):
    class Meta:
        model = CourseEnrollment
        exclude = ["has_completed", "is_active"]



