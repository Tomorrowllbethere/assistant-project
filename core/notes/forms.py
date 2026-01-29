import json
from django import forms
from .models import Note, Tag, NoteList

class NoteForm(forms.ModelForm):
    mixed_tags = forms.CharField(required=False, widget=forms.HiddenInput())
    
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=False
    )
    
    notebook = forms.ModelChoiceField(
        queryset=NoteList.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Оберіть блокнот"
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'start_date', 'end_date', 'notebook']

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data'].copy() 
            
            mixed_tags = data.get('mixed_tags', '')
            if mixed_tags and isinstance(mixed_tags, str) and mixed_tags.strip().startswith('['):
                try:
                    tag_data = json.loads(mixed_tags)
                    clean_values = []
                    for item in tag_data:
                        if isinstance(item, dict):
                            clean_values.append(item.get('value', ''))
                        else:
                            clean_values.append(str(item))
                    data['mixed_tags'] = ",".join(clean_values)
                    kwargs['data'] = data
                    
                except (json.JSONDecodeError, TypeError):
                    pass
        
        # 2. Стандартна ініціалізація
        self.user = kwargs.pop('user', None)
        super(NoteForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['notebook'].queryset = NoteList.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("Дата закінчення має бути пізніше дати початку.")
        return cleaned_data

    def save(self, commit=True):
        instance = super(NoteForm, self).save(commit=False)
        
        # 1. ПРИВ'ЯЗУЄМО ЮЗЕРА (Тепер це обов'язково і правильно)
        if self.user:
            instance.user = self.user
        
        # 2. Логіка дат
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if start_date and end_date:
            instance.expire_at = end_date - start_date
        
        # 3. Дефолтний блокнот (якщо не обрано)
        if not instance.notebook and self.user:
            default_notebook, created = NoteList.objects.get_or_create(
                list_name='Default Notebook',
                user=self.user 
            )
            instance.notebook = default_notebook

        if commit:
            instance.save()
            
            # 4. Теги
            tags_json = self.cleaned_data.get('mixed_tags')
            if tags_json:
                try:
                    tag_data = json.loads(tags_json)
                    tag_names = [t['value'] for t in tag_data]
                except:
                    tag_names = [t.strip() for t in tags_json.split(',')]
                
                new_tags_list = []
                for name in tag_names:
                    tag_obj, created = Tag.objects.get_or_create(tag=name)
                    new_tags_list.append(tag_obj)
                instance.tags.set(new_tags_list)
            
        return instance

# NotebookForm без змін
class NotebookForm(forms.ModelForm):
    list_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = NoteList
        fields = ['list_name']