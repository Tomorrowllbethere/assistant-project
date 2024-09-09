from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from custom_auth.models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    
    email = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Цей email вже використовується.")
        return email


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())
    date_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Виберіть дату'
        }),
        required=True,
        label='Виберіть дату'
    )
    address = forms.CharField(widget=forms.TextInput())



    class Meta:
        model = Profile
        fields = ['avatar', 'date_birth', 'address']
