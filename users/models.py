from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LogoutTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logout_time')
    logout = models.DateTimeField(blank=True, null=True)    