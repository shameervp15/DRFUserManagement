from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from notes.models import NotesModel

class NoteAPITest(APITestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        login_url = '/users/login/'
        login_data = {'username': self.username, 'password': self.password}
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data.get('access')
        self.assertIsNotNone(self.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.note1 = NotesModel.objects.create(title="NotesModel 1", description="Test description1", user=self.user)
        self.note2 = NotesModel.objects.create(title="NotesModel 2", description="Test description2", user=self.user)
        self.list_url = reverse('notes')
        self.detail_url = reverse('notes_detail', kwargs={'pk': self.note1.pk})

    def test_authenticated_user_can_list_notes(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) 

    def test_authenticated_user_can_create_note(self):
        data = {
            'title': 'New Test NotesModel',
            'description': 'New description.',
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NotesModel.objects.get(pk=response.data['id']).user, self.user)

    def test_owner_can_update_note(self):
        updated_data = {'title': 'Updated Title', 'description': self.note1.description}
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Updated Title')

    def test_owner_can_delete_note(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NotesModel.objects.count(), 1)