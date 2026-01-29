from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Q

from .models import Note, Tag, NoteList
from .forms import NoteForm, NotebookForm

# --- Autocomplete ---
def tags_autocomplete(request):
    term = request.GET.get('term', '')
    if len(term) < 2: return JsonResponse([], safe=False)
    tags = Tag.objects.filter(tag__icontains=term).values_list('tag', flat=True)[:10]
    return JsonResponse(list(tags), safe=False)

# --- Notebooks ---
@login_required
def create_notelist(request):
    if request.method == "POST":
        form = NotebookForm(request.POST)
        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()
            return redirect('notes:notebook-list')
    else:
        form = NotebookForm()
    return render(request, 'notes/notebook_form.html', {'form': form})

@login_required
def notebook_list(request):
    # 1. Завантажуємо блокноти у список
    notebooks = list(NoteList.objects.filter(user=request.user))
    
    for notebook in notebooks:
        # 2. Шукаємо нотатки. Тепер у нас подвійний захист:
        # і по notebook, і по user (це надійно).
        notebook.notes = Note.objects.filter(notebook=notebook, user=request.user)
        
    return render(request, 'notes/notebook_list.html', {'notebooks': notebooks})

class NotebookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NoteList
    fields = ['list_name']
    template_name = 'notes/notebook_form.html' 
    success_url = reverse_lazy('notes:notebook-list')
    def test_func(self): return self.request.user == self.get_object().user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Notebook'
        return context

class NotebookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NoteList
    template_name = 'notes/notebook_confirm_delete.html'
    success_url = reverse_lazy('notes:notebook-list')
    def test_func(self): return self.request.user == self.get_object().user

# --- Notes ---
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:notebook-list')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:notebook-list')
    # Перевірка проста: це моя нотатка?
    def test_func(self): return self.request.user == self.get_object().user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note  
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:notebook-list')
    def test_func(self): return self.request.user == self.get_object().user

# --- Lists & Detail ---
@login_required
def all_note_list(request):
    # Просто і чисто: всі мої нотатки
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_detail(request, pk):
    # Захист: тільки якщо user=я
    note = get_object_or_404(Note, pk=pk, user=request.user)
    
    current_time = timezone.now()
    time_diff = None
    time_diff_sec = None
    if note.start_date and note.start_date > current_time:
        time_diff = note.start_date - current_time
        time_diff_sec = time_diff.total_seconds()
    elif note.end_date:
        time_diff = note.end_date - current_time
        time_diff_sec = time_diff.total_seconds()

    return render(request, 'notes/note_detail.html', {
        'note': note, 'now': current_time,
        'time_diff': time_diff, 'time_diff_sec': time_diff_sec
    })

@login_required
def tag_search(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    # Шукаємо мої нотатки з цим тегом
    notes = Note.objects.filter(tags__id=pk, user=request.user)
    return render(request, "notes/note_list.html", context={"notes": notes, "tag": tag})

class NoteSearchView(LoginRequiredMixin, ListView):
    model = Note  
    template_name = 'notes/note_search.html'
    context_object_name = 'notes'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query: return Note.objects.none()
        return Note.objects.filter(user=self.request.user).filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__tag__icontains=query)
        ).distinct()