from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.notebook_list, name='notebook-list'),
    path('notebook/', views.create_notelist, name='notebook-create'),
    path('notes/', views.all_note_list, name='all-notes'),
    path('notebook/<int:pk>/edit/', views.NotebookUpdateView.as_view(), name='notebook-edit'),
    path('notebook/<int:pk>/delete/', views.NotebookDeleteView.as_view(), name='notebook-delete'),
    path('create/', views.NoteCreateView.as_view(), name='note-create'),
    path('<int:pk>/', views.note_detail, name='note-detail'),
    path('<int:pk>/update/', views.NoteUpdateView.as_view(), name='note-update'),
    path('<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note-delete'),
    path('search/', views.NoteSearchView.as_view(), name='note-search'),
    path('<int:pk>/search/', views.tag_search, name='tag-search'),
    path('tags-autocomplete/', views.tags_autocomplete, name='tags-autocomplete'),
]

