# Devbotapp/models.py

from django.db import models
from django.contrib.auth.models import User

# Devbotapp/models.py

from django.db import models
from django.contrib.auth.models import User


class Logo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='logos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name}'s Logo"