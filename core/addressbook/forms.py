from django import forms
from django.forms import inlineformset_factory
from addressbook.models import AllContact, Phone, Email
from core import settings
import cloudinary

class AllContactForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Виберіть дату'
        }),
        required=True,
        label='Виберіть дату'
    )
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Завантажити власний аватар'
    )
    
    avatar_url = forms.ChoiceField(
        choices=[('female', 'Avatar 1'), ('male', 'Avatar 2'), ('neutral', 'Avatar 3')],
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'avatar-choice'})
    )

    

    class Meta:
        model = AllContact
        fields = ['fullname', 'address', 'birthday', 'avatar', 'avatar_url']

    def clean(self):
        cleaned_data = super().clean()
        avatar_url = cleaned_data.get("avatar_url")
        avatar = cleaned_data.get("avatar")

        # Якщо не вибрано ні аватар із списку, ні завантажено власний
        if not avatar_url and not avatar:
            raise forms.ValidationError("Будь ласка, виберіть аватар або завантажте власний.")
        
        return cleaned_data


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['ntel']

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['mail']

PhoneFormSet = inlineformset_factory(AllContact, Phone, form=PhoneForm, extra=1, can_delete=True)
EmailFormSet = inlineformset_factory(AllContact, Email, form=EmailForm, extra=1, can_delete=True)
