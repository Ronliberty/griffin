# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class StaffCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff']

    def clean_is_staff(self):
        is_staff = self.cleaned_data.get('is_staff', False)
        if not self.request.user.is_superuser:
            raise forms.ValidationError("Only superusers can create staff members.")
        return is_staff
