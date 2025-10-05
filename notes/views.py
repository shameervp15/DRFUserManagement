from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.filters import SearchFilter

from notes.serializers import NotesSerializer
from notes.models import NotesModel
from notes.pagination import NotesPagination


class NotesListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotesSerializer
    pagination_class = NotesPagination

    filter_backends = (SearchFilter, )
    search_fields = ('title', 'description')

    ordering_fields = ('created_at', 'title')
    # ordering = ('-created_at',)

    def get_queryset(self):
        return NotesModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotesModel.objects.filter(user=self.request.user)

