from django import forms
from django.contrib.auth.models import User
from .models import Profile, Order

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    is_delivery_person = forms.BooleanField(required=False, label="Register as delivery person")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned

class UpdateLocationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['latitude', 'longitude']
