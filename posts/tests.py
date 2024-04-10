from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_retrieve_post(self):
        adam = User.objects.get(username='adam')
        post = Post.objects.create(owner=adam, title='a title')
        response = self.client.get(f'/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_post(self):
        adam = User.objects.get(username='adam')
        post = Post.objects.create(owner=adam, title='a title')
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            f'/posts/{post.id}/', {'title': 'new title'})
        post.refresh_from_db()
        self.assertEqual(post.title, 'new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_cant_update_post(self):
        adam = User.objects.get(username='adam')
        post = Post.objects.create(owner=adam, title='a title')
        response = self.client.put(
            f'/posts/{post.id}/', {'title': 'new title'})
        post.refresh_from_db()
        self.assertEqual(post.title, 'a title')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
