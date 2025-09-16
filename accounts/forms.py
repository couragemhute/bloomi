from django import forms
from accounts.models import CustomUser
from blog.forms import StyledModelForm

class CustomUserForm(StyledModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

