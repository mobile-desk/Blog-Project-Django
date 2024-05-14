from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_new'), {
            'title': 'New Post',
            'content': 'New content',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_edit', args=[self.post.id]), {
            'title': 'Updated Post',
            'content': 'Updated content',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
