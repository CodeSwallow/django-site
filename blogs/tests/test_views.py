import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from blogs.models import (
    Post,
    Category,
    Comment,
)


def create_user(username='new_user', password='test_pass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(username, password)


class HomePageViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_posts = 13
        author = create_user()

        past_date = timezone.now() - datetime.timedelta(days=13)
        for i in range(number_of_posts):
            Post.objects.create(
                title=f'Django Post {i}',
                slug=f'django-post-{i}',
                overview='Create a django blog',
                content='Content of django blog tutorial',
                table_of_contents='table...',
                pub_date=past_date + datetime.timedelta(days=i),
                author=author,
                featured=i%2,
            )
        future_date = timezone.now() + datetime.timedelta(days=1)
        cls.future_post = Post.objects.create(
            title=f'Django Post Future',
            slug=f'django-post-future',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=future_date,
            author=author
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertTemplateUsed(response, 'blogs/homepage.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['post_list']), 10)

    def test_lists_all_posts(self):
        """Tests second page has remaining posts"""
        response = self.client.get(reverse('blogs:home') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['post_list']), 3)

    def test_post_are_ordered_from_latest(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post_list'][0].pub_date.date(), (timezone.now() - datetime.timedelta(days=1)).date())

    def test_future_post_is_not_shown(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.future_post, response.context['post_list'])

    def test_featured_posts_are_present(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('featured' in response.context)

    def test_only_three_featured_post_are_present(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['featured']), 3)

    def test_categories_are_present(self):
        response = self.client.get(reverse('blogs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('categories' in response.context)


class PostDetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='Django Blog',
            slug='django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=timezone.now() - datetime.timedelta(days=1),
            author=create_user()
        )
        future_date = timezone.now() + datetime.timedelta(days=1)
        cls.future_post = Post.objects.create(
            title='Future Django Blog',
            slug='future-django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=future_date,
            author=create_user(username='user1')
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/post/django-blog')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs:post', kwargs={'slug':self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs:post', kwargs={'slug':self.post.slug}))
        self.assertTemplateUsed(response, 'blogs/post_detail.html')

    def test_future_post_is_not_shown(self):
        response = self.client.get(reverse('blogs:post', kwargs={'slug': self.future_post.slug}))
        self.assertEqual(response.status_code, 404)

    def test_categories_are_present(self):
        response = self.client.get(reverse('blogs:post', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('categories' in response.context)

    def test_comment_form_is_present(self):
        response = self.client.get(reverse('blogs:post', kwargs={'slug':self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)


class PostCommentFormViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user(username='user1')
        cls.post = Post.objects.create(
            title='Django Blog',
            slug='django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=timezone.now() - datetime.timedelta(days=1),
            author=create_user()
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('blogs:post', kwargs={'slug':self.post.slug}), {'description': 'New comment'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_user_can_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('blogs:post', kwargs={'slug':self.post.slug}), {'description': 'New comment'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/post/'))

    def test_redirects_to_posted_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('blogs:post', kwargs={'slug':self.post.slug}),
                                    {'description': 'New comment'})
        self.assertRedirects(response, reverse('blogs:post', kwargs={'slug':self.post.slug}) + '#comments-section')


class CategoryViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = create_user()
        cls.category = Category.objects.create(
            title='django',
            slug='django-framework'
        )
        Category.objects.create(
            title='python',
            slug='python'
        )
        post_1 = Post.objects.create(
            title='Django Blog',
            slug='django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=timezone.now() - datetime.timedelta(days=1),
            author=user
        )
        post_2 = Post.objects.create(
            title='Django Something',
            slug='django-something',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=timezone.now() - datetime.timedelta(days=1),
            author=user
        )
        other_category_post = Post.objects.create(
            title='Python Something',
            slug='python-something',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=timezone.now() - datetime.timedelta(days=1),
            author=user
        )
        future_post = Post.objects.create(
            title='Future Django Blog',
            slug='future-django-blog',
            overview='Create a django blog',
            content='Content of django blog tutorial',
            table_of_contents='table...',
            pub_date=timezone.now() + datetime.timedelta(days=1),
            author=user
        )

        post_categories = Category.objects.all()
        post_1.categories.set(post_categories)
        post_1.save()

        django_category = Category.objects.get(slug='django-framework')
        post_2.categories.add(django_category)
        post_2.save()

        python_category = Category.objects.get(slug='python')
        other_category_post.categories.add(python_category)
        other_category_post.save()

        future_post.categories.set(post_categories)
        future_post.save()

        cls.future_post = future_post

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/django-framework')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs:category', kwargs={'slug':self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs:category', kwargs={'slug':self.category.slug}))
        self.assertTemplateUsed(response, 'blogs/category_view.html')

    def test_future_posts_are_not_shown(self):
        response = self.client.get(reverse('blogs:category', kwargs={'slug': self.category.slug}))
        self.assertNotIn(self.future_post, response.context['post_list'])

    def test_correct_amount_is_shown(self):
        """Assert only 2 post are shown (future posts and other categories excluded)"""
        response = self.client.get(reverse('blogs:category', kwargs={'slug': self.category.slug}))
        self.assertEqual(len(response.context['post_list']), 2)

    def test_categories_are_present(self):
        response = self.client.get(reverse('blogs:category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('categories' in response.context)


