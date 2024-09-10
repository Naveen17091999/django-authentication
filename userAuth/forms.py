from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False, label='Phone Number')
    age = forms.IntegerField(required=False, label='Age')
    date_of_birth = forms.DateField(required=False, label='Date of Birth')
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, label='Gender')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Include these fields in the form

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number'),
                age=self.cleaned_data.get('age'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender')
            )
        return user

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive")

        return cleaned_data