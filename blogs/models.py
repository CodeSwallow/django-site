from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


class Series(models.Model):
    """Post series including various posts"""
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)

    def get_absolute_url(self):
        """Returns the URL to access a particular series instance."""
        return reverse("blogs:series-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Post(models.Model):
    """Model for blog posts."""
    # TODO: look into serving media through markdown content
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    overview = models.TextField(_("overview"))
    thumbnail = models.ImageField(_("thumbnail"), upload_to='thumbnails/', blank=True, null=True)
    content = models.TextField(_("content"))
    table_of_contents = models.TextField(_("table of contents"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    featured = models.BooleanField(_("featured"), default=False)
    active = models.BooleanField(_("active"), default=True)
    pub_date = models.DateTimeField(_('publish date'), default=timezone.now)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published?',
    )
    def published(self):
        """Determines if the post has been published yet."""
        return self.pub_date < timezone.now()

    def get_absolute_url(self):
        """Returns the URL to access a particular post instance."""
        return reverse("blogs:post", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    """Blog category."""
    title = models.CharField(_("title"), max_length=20)
    slug = models.SlugField(_("slug"), unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        """Returns the URL to access a particular category instance."""
        return reverse("blogs:category", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Blog Comment"""
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        len_title = 75
        if len(self.description) > len_title:
            return self.description[:len_title] + '...'
        else:
            return self.description
