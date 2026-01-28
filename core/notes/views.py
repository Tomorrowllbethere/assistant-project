from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note, Tag, NoteList
from .forms import NoteForm, NotebookForm

from django.utils import timezone
import datetime as dt
now = timezone.now()

@login_required
def create_notelist(request):
    if request.method == "POST":
        form = NotebookForm(request.POST)
        if form.is_valid(): # Тепер це пройде!
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()
            return redirect('notes:notebook-list')
    else:
        form = NotebookForm()
    return render(request, 'notes/notebook_form.html', {'form': form})


@login_required
def notebook_list(request):
    notebooks = NoteList.objects.all()
    notes = Note.objects.all()
    for notebook in notebooks:
        notebook.notes = notebook.notebook.all()
    return render(request, 'notes/notebook_list.html', {'notebooks': notebooks})

#для відображення списку нотаток
def all_note_list(request):
    notes = Note.objects.all()
    if notes is False:
        notes=[]
    return render(request, 'notes/note_list.html', {'notes': notes})

#для відображення деталей окремої нотатки
# class NoteDetailView(DetailView):
#     model = Note
#     template_name = 'notes/note_detail.html'

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    # Calculate difference between now and start_date or end_date
    if note.start_date > now:
        time_diff = note.start_date - now
        time_diff_sec = time_diff.total_seconds
    elif note.end_date:
        time_diff = note.end_date - now
        time_diff_sec = time_diff.total_seconds
    else:
        time_diff = None
        time_diff_sec = None

    return render(request, 'notes/note_detail.html', {
        'note': note,
        'now': now,
        'time_diff': time_diff,
        'time_diff_sec' :time_diff_sec
    })

def tag_search(request, pk):
    tag_name = Tag.objects.filter(id=pk).get()
    notes = Note.objects.filter(tags__id=pk).all()
    return render(request, "notes/note_list.html", context={"notes":notes, "tag":tag_name})

# Клас для створення нової нотатки
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:notebook-list')

    def form_valid(self, form):
        response = super().form_valid(form)  # Зберігаємо форму і отримуємо відповідь
        new_tags = self.request.POST.get('new_tags')  # Отримуємо нові теги з POST-запиту
        if new_tags:
            tags = [tag.strip() for tag in new_tags.split(',')]  # Розділяємо і очищуємо теги
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(tag=tag)  # Перевіряємо і створюємо теги
                self.object.tags.add(tag_obj)  # Додаємо теги до нотатки
        return response  # Повертаємо відповідь


# Клас для оновлення існуючої нотатки
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:notebook-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        new_tags = self.request.POST.get('new_tags')
        if new_tags:
            tags = [tag.strip() for tag in new_tags.split(',')]
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(tag=tag)
                self.object.tags.add(tag_obj)
        return response


# Клас для видалення нотатки
class NoteDeleteView(DeleteView):
    model = Note  
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note-list')


# Клас для пошуку нотаток
class NoteSearchView(ListView):
    model = Note  
    template_name = 'notes/note_search.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('q')  
        return Note.objects.filter(
            title__icontains=query) | Note.objects.filter(
            content__icontains=query) | Note.objects.filter(
            tags__tag__icontains=query).distinct()  # Пошук нотаток за заголовком, вмістом і тегами