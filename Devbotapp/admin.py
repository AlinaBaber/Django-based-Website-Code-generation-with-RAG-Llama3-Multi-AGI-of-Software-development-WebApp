# Devbotapp/admin.py

from django.contrib import admin
from .models import Question, Option, UserResponse

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserResponse)
