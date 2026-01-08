from django import forms

from blog.forms import StyledModelForm
from blog.models import Subscriber
from .models import Course, Expert, CourseRating


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


class CourseRatingForm(forms.ModelForm):
    class Meta:
        model = CourseRating
        fields = ['course', 'stars', 'comment']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }

    def __init__(self,  *args, **kwargs):
        super(CourseRatingForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"