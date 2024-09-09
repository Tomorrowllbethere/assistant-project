from django.urls import path
from . import views

app_name = 'addressbook'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('birthday_list/', views.birthday_list, name='birthday_list'),
    path('search_contact/', views.search_contact, name='search_contact'),
    path('contact_list/', views.contact_list, name='contact_list'),
    path('edit_contact/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('delete_contact/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('profile/<int:pk>/', views.contact_profile, name='profile-contact')
]
