from django import forms
from role.models import Role
from django.contrib.auth.models import Permission


class YesNoSelect(forms.Select):
    def __init__(self, attrs=None):
        choices = (
            (True, 'Yes'),
            (False, 'No')
        )
        super().__init__(attrs, choices=choices)

    def format_value(self, value):
        if value is None:
            return ''
        return str(value)

class RoleForm(forms.ModelForm):
    is_admin = forms.BooleanField(widget=YesNoSelect, required=False)

    class Meta:
        model = Role
        exclude = ['code']
        
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
