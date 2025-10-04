from django.db import models
from django.contrib.auth.models import User

class NotesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='note_attachments/', null=True, blank=True)

    def __str__(self):
        return self.title