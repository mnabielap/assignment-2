from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
