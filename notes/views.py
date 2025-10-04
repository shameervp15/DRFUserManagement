from django.shortcuts import render
from notes.serializers import NotesSerializer
from notes.models import NotesModel
from rest_framework import viewsets, permissions, generics


class NotesListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotesSerializer

    def get_queryset(self):
        return NotesModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print(serializer)
        serializer.save(user=self.request.user)

class NotesDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotesModel.objects.filter(user=self.request.user)

