# Devbotapp/models.py

from django.db import models
from django.contrib.auth.models import User

# Devbotapp/models.py

from django.db import models
from django.contrib.auth.models import User

class ProjectType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Question(models.Model):
    QUESTION_TYPES = [
        ('combo', 'Combo Box'),
        ('checkbox', 'Check Box'),
    ]

    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    project_type = models.ForeignKey(ProjectType, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text



class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,default=1)
    selected_options = models.ManyToManyField(Option, related_name='selected_options', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"
class Logo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='logos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name}'s Logo"

class UIRequirement(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    font = models.CharField(max_length=255)
    font_color = models.CharField(max_length=7)
    color_palette = models.JSONField(null=True, blank=True)
    color_choice = models.CharField(max_length=20, choices=[('Generated', 'Generated'), ('Customized', 'Customized')], default='Generated')

    def __str__(self):
        return f'UI Requirements for {self.project.name}'

class TechnicalRequirement(models.Model):
    DEVELOPMENT_FRAMEWORKS_CHOICES = [
        ('Static HTML', 'Static HTML'),
        ('Django', 'Django'),
        ('Laravel', 'Laravel'),
        ('ASP.NET Core', 'ASP.NET Core'),
        ('Angular', 'Angular'),
        ('React', 'React'),
        ('Vue.js', 'Vue.js'),
        ('Flask', 'Flask'),
        ('Meteor', 'Meteor'),
        ('Svelte', 'Svelte'),
        ('Next.js', 'Next.js'),
        ('Nuxt.js', 'Nuxt.js'),
        ('Phoenix', 'Phoenix'),
        ('CodeIgniter', 'CodeIgniter'),
        ('CakePHP', 'CakePHP'),
        ('Symfony', 'Symfony'),
        ('Play Framework', 'Play Framework'),
        ('Koa.js', 'Koa.js'),
    ]

    CMS_CHOICES = [
        ('WordPress', 'WordPress'),
        ('Joomla', 'Joomla'),
        ('Drupal', 'Drupal'),
        ('Magento', 'Magento'),
        ('Shopify', 'Shopify'),
        ('Squarespace', 'Squarespace'),
        ('Wix', 'Wix'),
        ('Weebly', 'Weebly'),
        ('TYPO3', 'TYPO3'),
        ('Ghost', 'Ghost'),
        ('Umbraco', 'Umbraco'),
        ('Sitecore', 'Sitecore'),
        ('Craft CMS', 'Craft CMS'),
        ('Concrete5', 'Concrete5'),
        ('Contentful', 'Contentful'),
        ('Strapi', 'Strapi'),
        ('October CMS', 'October CMS'),
        ('SilverStripe', 'SilverStripe'),
        ('HubSpot CMS', 'HubSpot CMS'),
        ('Webflow', 'Webflow'),
        ('Customized', 'Customized'),
    ]

    development_framework = models.CharField(max_length=50, choices=DEVELOPMENT_FRAMEWORKS_CHOICES)
    cms = models.CharField(max_length=50, choices=CMS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technical_requirements')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.development_framework} - {self.cms}"

from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    LLM_CHOICES = [
        ('llama3', 'Llama3'),
        ("gpt-4", 'GPT-4'),
        ("gpt-4o", 'GPT-4o'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='botrequirements')
    llm = models.CharField(max_length=50, choices=LLM_CHOICES, default='llama3')

    def __str__(self):
        return f"{self.user.username}'s Bot ({self.llm_choice})"
