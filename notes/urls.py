from django.urls import path
from notes.views import NotesListCreateView, NotesDetailsView

urlpatterns = [
    path('', NotesListCreateView.as_view(), name='notes'),
    path('<int:pk>/', NotesDetailsView.as_view(), name='notes_detail'),
]