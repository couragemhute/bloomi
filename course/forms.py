from django import forms

from blog.forms import StyledModelForm
from blog.models import Subscriber
from .models import Course, Expert


class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "image", "price", "level"]


class SubscriberForm(StyledModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]


class ExpertForm(StyledModelForm):
    class Meta:
        model = Expert
        fields = ["name", "role", "bio", "photo"]
