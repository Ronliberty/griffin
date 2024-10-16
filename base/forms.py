from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Form to handle project details
class CompleteProjectForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter project description...'
        }),
        label='Project Description',
        max_length=1000
    )
    file = forms.FileField(
        label='Upload File (optional)',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Choose a file...'
        })
    )

# Form to edit user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'fb_url', 'twitter_url']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'placeholder': 'Upload your profile picture...'
            }),
            'fb_url': forms.URLInput(attrs={
                'placeholder': 'Facebook URL'
            }),
            'twitter_url': forms.URLInput(attrs={
                'placeholder': 'Twitter URL'
            }),
        }

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'placeholder': 'Upload your profile picture...'
            })
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
        }
