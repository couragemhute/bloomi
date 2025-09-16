from django import forms
from .models import Category, Blog


class StyledModelForm(forms.ModelForm):
    """Base form to add Bootstrap form-control to all fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class CategoryForm(StyledModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class BlogForm(StyledModelForm):
    class Meta:
        model = Blog
        fields = ["title", "category", "image", "content"]

