from django.contrib import admin
from blogs.models import (
    Post,
    Category,
    Series,
    Comment
)

admin.site.register(Category)
admin.site.register(Series)
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'published')
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
