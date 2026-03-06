from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password',
        required=True
    )
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    pincode = forms.CharField(max_length=15, required=True)
    personal_id = forms.CharField(max_length=20, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            # User exists — check if profile exists
            try:
                _ = user.profile
                # Profile exists — username truly taken
                raise forms.ValidationError('This username is already taken.')
            except Profile.DoesNotExist:
                # Orphaned user — delete it so registration can proceed
                user.delete()
        except User.DoesNotExist:
            pass  # username is free — good
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_personal_id(self):
        personal_id = self.cleaned_data.get('personal_id')
        if Profile.objects.filter(personal_id=personal_id).exists():
            raise forms.ValidationError('This personal ID is already registered.')
        return personal_id

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data