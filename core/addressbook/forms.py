from django import forms
from django.forms import inlineformset_factory
from .models import AllContact, Phone, Email

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
    class Meta:
        model = AllContact
        fields = ['fullname', 'address', 'birthday']

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
