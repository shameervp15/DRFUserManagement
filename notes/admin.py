from django.contrib import admin
from notes.models import NotesModel
from users.models import UserProfileModel

admin.site.register(NotesModel)
admin.site.register(UserProfileModel)
