from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth import get_user_model

from blogs.models import Post


def create_user(email='user@example.com', password='test_pass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class MarkdownExtrasTests(TestCase):
    """Test for markdown extras template tags."""
    body_content = """## Another Header with more Stuff"""
    table_of_contents = """[TOC]\n# [First Header of Content](#first-header-of-content)"""

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='Django Blog',
            slug='django-blog',
            overview='Create a django blog',
            content=cls.body_content,
            table_of_contents=cls.table_of_contents,
            author=create_user()
        )

    def test_markdown(self):
        out = Template(
            "{% load markdown_extras %}"
            "{{ post.content | markdown | safe }}"
        ).render(Context({"post": self.post}))
        self.assertEqual(out, '<h2 id="another-header-with-more-stuff">Another Header with more Stuff</h2>')

    def test_markdown_toc(self):
        out = Template(
            "{% load markdown_extras %}"
            "{{ post.table_of_contents | markdown_toc | safe }}"
        ).render(Context({"post": self.post}))
        self.assertEqual(out, """<div class="toc">\n<ul>\n<li><a href="#first-header-of-content">First Header of Content</a></li>\n</ul>\n</div>""")
