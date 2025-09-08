from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='user_obj', on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)