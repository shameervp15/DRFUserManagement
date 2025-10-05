from rest_framework import serializers
from notes.models import NotesModel

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        # fields = '__all__'
        fields = ['id', 'title', 'created_at', 'modified_at', 'description', 'attachment']
        read_only_fields = ['id', 'created_at', 'modified_at']