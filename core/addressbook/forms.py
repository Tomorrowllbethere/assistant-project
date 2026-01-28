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
    avatar = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Завантажити власне фото'
    )
    # Це поле прийме URL обраного пресета. Ми робимо його CharField, 
    # бо JS запише туди повний шлях до картинки.
    avatar_url = forms.CharField(
        required=False, 
        widget=forms.HiddenInput() 
    )

    

    class Meta:
        model = AllContact
        fields = ['fullname','gender', 'address', 'birthday', 'avatar', 'avatar_url']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}), # Випадаючий список
        }

    def clean(self):
        cleaned_data = super().clean()
        avatar_url = cleaned_data.get("avatar_url")
        avatar = cleaned_data.get("avatar")

        
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
