from django import forms
from .models import Note, Tag, NoteList



class NoteForm(forms.ModelForm):
    new_tags = forms.CharField(max_length=255, required=False, help_text='Введіть нові теги через кому')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    notebook = forms.ModelChoiceField(
        queryset=NoteList.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Виберіть блок нотаток або залиште порожнім, щоб використати блок за замовчуванням"
    )
    class Meta:
        model = Note
        fields = ['title', 'content',  'start_date', 'end_date', 'tags']

    def clean(self):
        cleaned_data = super().clean()
         
        return cleaned_data


    def save(self, commit=True):
        instance = super(NoteForm, self).save(commit=False)
        new_tags = self.cleaned_data.get('new_tags', '')
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        print(start_date, end_date)
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date must be after start date.")   
            # Calculate the duration (expires_at) as the difference between end_date and start_date
            instance.expire_at = end_date - start_date
        if not instance.notebook:
            # Якщо блок нотаток не обраний, встановлюємо блок за замовчуванням
            default_notebook, created = NoteList.objects.get_or_create(list_name='Default Notebook')
            instance.notebook = default_notebook
        if commit:
            instance.save()
            if new_tags:
                tag_names = [name.strip() for name in new_tags.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(tag=tag_name)
                    instance.tags.add(tag)
            self.save_m2m()
        return instance
    
class NotebookForm(forms.ModelForm):
    list_name = forms.CharField(max_length=255, required=False, help_text='Додайте новий блок нотаток')

    class Meta:
        model = NoteList
        fields = ['list_name']
    def clean(self):
        cleaned_data = super().clean()
            # Видаляємо помилку про юзера, бо ми додамо його у views.py
        if 'user' in self._errors:
            del self._errors['user']
        return cleaned_data
        