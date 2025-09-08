from django.db import models

from usermanagement.models import UserProfile


class Snippet(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField()
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='snippets')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title