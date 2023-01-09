import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from blogs.models import (
    Post,
    Category,
    Series,
    Comment,
)


def create_user(email='user@example.com', password='test_pass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class PostModelTest(TestCase):
    """Test for post model."""

    @classmethod
    def setUpTestData(cls):
        user = create_user()
        Post.objects.create(
            title='Django Blog',
            slug='django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            author=user
        )
        future_date = timezone.now() + datetime.timedelta(days=1)
        cls.future_post = Post.objects.create(
            title='Future Django Blog',
            slug='future-django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=future_date,
            author=user
        )

    def test_object_name_is_title(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), 'Django Blog')

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), '/post/django-blog')

    def test_published_post_returns_true(self):
        """Returns True is date is less or equal to now"""
        post = Post.objects.get(id=1)
        self.assertTrue(post.published())

    def test_future_date_returns_published_false(self):
        """Returns False if date is in the future"""
        self.assertFalse(self.future_post.published())


class CategoryModelTest(TestCase):
    """Test for post category model."""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(
            title='django',
            slug='django'
        )

    def test_object_name_is_title(self):
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), 'django')

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), '/category/django')


class SeriesModelTest(TestCase):
    """Test for post series model."""

    @classmethod
    def setUpTestData(cls):
        Series.objects.create(
            title='Django Blog Series',
            slug='django-blog-series'
        )

    def test_object_name_is_title(self):
        series = Series.objects.get(id=1)
        self.assertEqual(str(series), 'Django Blog Series')

    def test_get_absolute_url(self):
        series = Series.objects.get(id=1)
        self.assertEqual(series.get_absolute_url(), '/series/django-blog-series')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='Django Blog',
            slug='django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            author=create_user()
        )

    def test_object_name_is_description(self):
        comment = Comment.objects.create(
            description='this is a description',
            author=create_user(email='new_email@example.com'),
            post=self.post,
        )
        self.assertEqual(str(comment), 'this is a description')

    def test_object_name_does_not_exceed_75_characters(self):
        """Object name will print a max 75 description characters plus three dots (...), so a total of 78 characters"""
        comment = Comment.objects.create(
            description=''.join([str(i) for i in range(100)]),
            author=create_user(email='new_email@example.com'),
            post=self.post,
        )
        self.assertEqual(len(str(comment)), 78)
        self.assertIn('...', str(comment))

