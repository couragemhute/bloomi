from django import forms

from blog.forms import StyledModelForm
from blog.models import Subscriber
from .models import Course, Expert


class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        exclude = ["slug", "is_active"]


class SubscriberForm(StyledModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]


class ExpertForm(StyledModelForm):
    class Meta:
        model = Expert
        fields = ["course", "user", "start_date"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }
