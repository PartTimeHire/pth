from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobRequest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
