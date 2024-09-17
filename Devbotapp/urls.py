# Devbotapp/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'Devbotapp'
urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('home/', views.home_view, name='home'),
    path('create_project/', views.create_project_view, name='create_project'),
    path('question/<int:question_id>/', views.userrequirements_view, name='userrequirements'),
    path('upload_logo/', views.upload_logo_view, name='upload_logo'),
    path('select_project_type/', views.create_project_view, name='select_project_type'),  # Ensure this is defined
    path('logout/', views.custom_logout_view, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('email_change/', views.email_change_view, name='email_change'),
    path('build_by_chat/', views.build_by_chat_view, name='build_by_chat'),
    path('signup/', views.signup_view, name='signup'),
    path('save_color_palette/', views.save_color_palette_view, name='save_color_palette'),
    path('project/<int:project_id>/ui_requirements/', views.ui_requirements_view, name='ui_requirements'),
    path('project/<int:project_id>/technical_requirement/', views.technical_requirement_view,name='technical_requirement'),
    path('project/<int:project_id>/details/', views.project_details_view, name='project_details'),
    path('project/<int:project_id>/code_generation/',views.code_generation_view, name='code_generation'),
    path('project/<int:project_id>/display_view/', views.display_view, name='display_view'),
    path('project/<int:project_id>/start_code_generation/', views.start_code_generation, name='start_code_generation'),
    path('project/<int:project_id>/display_site/', views.display_generated_site, name='display_generated_site'),
    path('project/<int:project_id>/download_zip/', views.download_project_zip, name='download_project_zip'),
    path('project/<int:project_id>/download_documents/', views.download_project_documents, name='download_project_documents'),
]