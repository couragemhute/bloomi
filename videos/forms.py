# videos/forms.py
from django import forms

class VideoPromptForm(forms.Form):
    prompt = forms.CharField(
        label="Enter a prompt for your AI video",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Describe the scene you want..."}),
    )
