from django.contrib import admin

# Register your models here.

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'date_posted']
    search_fields = ['user__username', 'place__title', 'content']
