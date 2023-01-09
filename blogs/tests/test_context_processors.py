from django.test import TestCase
from django.urls import reverse

from blogs.models import Category


class CategoryProcessorTest(TestCase):
    """Test for custom category context processor."""

    def test_categories_are_in_context(self):
        post = Category.objects.create(
            title='django',
            slug='django-framework'
        )
        response = self.client.get(reverse('blogs:home'))
        self.assertIn(post, response.context['categories'])
        self.assertEquals(len(response.context['categories']), 1)

    def test_correct_category_count_is_in_context(self):
        Category.objects.create(
            title='django',
            slug='django-framework'
        )
        Category.objects.create(
            title='python',
            slug='python'
        )
        response = self.client.get(reverse('blogs:home'))
        self.assertEquals(len(response.context['categories']), 2)
