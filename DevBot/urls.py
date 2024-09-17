# questionnaire/urls.py

from django.contrib import admin
from django.urls import include, path
from Devbotapp import views as userrequirements_view
from Devbotapp.views import get_project_requirements

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's built-in auth views
    path('', include('Devbotapp.urls')),  # Ensure this points to your app's URL configuration
    path('', userrequirements_view.welcome_view, name='welcome'),
    path('api/project_requirements/<int:project_id>/', get_project_requirements, name='project_requirements'),
]
