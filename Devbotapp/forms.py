# Devbotapp/forms.py

from django import forms
from django.utils.safestring import mark_safe

from .models import Question, Option, UserResponse, UIRequirement
from django import forms
from .models import Project, Logo,ProjectType, TechnicalRequirement
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Devbotapp.Client.models import Client
class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_type']

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        if question.question_type == 'combo':
            self.fields['answer'] = forms.ChoiceField(
                choices=[(option.id, option.text) for option in question.options.all()],
                widget=forms.Select,
                label=question.text
            )
        elif question.question_type == 'checkbox':
            self.fields['answer'] = forms.MultipleChoiceField(
                choices=[(option.id, option.text) for option in question.options.all()],
                widget=forms.CheckboxSelectMultiple,
                label=question.text
            )

    def save_response(self, user):
        data = self.cleaned_data['answer']
        if self.question.question_type == 'combo':
            selected_option = Option.objects.get(id=data)
            UserResponse.objects.create(user=user, question=self.question, selected_option=selected_option)
        elif self.question.question_type == 'checkbox':
            selected_options = Option.objects.filter(id__in=data)
            response = UserResponse.objects.create(user=user, question=self.question)
            response.selected_options.set(selected_options)

from django import forms
from .models import Question, Option

from django import forms
from .models import UserResponse, Question

class DynamicQuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(DynamicQuestionForm, self).__init__(*args, **kwargs)
        self.question = question

        options = question.options.all()

        if question.question_type == 'combo':
            self.fields['answer'] =forms.ChoiceField(choices=[(option.id, option.text) for option in question.options.all()],
                label=question.text)
        elif question.question_type == 'checkbox':
            self.fields['answer'] = forms.MultipleChoiceField(
                choices=[(option.id, option.text) for option in question.options.all()],
                widget=forms.CheckboxSelectMultiple,
                label=question.text
            )
        else:
            self.fields['answer'] = forms.CharField(widget=forms.Textarea)

    def save_response(self, user, project):
        answer = self.cleaned_data['answer']
        if self.question.question_type == 'checkbox':
            response = UserResponse.objects.create(
                user=user,
                question=self.question,
                project=project
            )
            response.selected_options.set(answer)
        else:
            selected_option = Option.objects.get(id=answer)
            UserResponse.objects.create(
                user=user,
                question=self.question,
                selected_option=selected_option,
                project=project
            )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'project_type','description']

class LogoUploadForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ['image']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    client_type = forms.ChoiceField(choices=Client.CLIENT_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'client_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                email=user.email,
                client_type=self.cleaned_data['client_type']
            )
        return user


class ColorChoiceForm(forms.Form):
    COLOR_CHOICES = [
        ('Generated', 'Generated'),
        ('Customized', 'Customized')
    ]

    color_choice = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.RadioSelect)
    custom_color_palette = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), required=False)

    def __init__(self, *args, **kwargs):
        generated_palette = kwargs.pop('generated_palette', [])
        super(ColorChoiceForm, self).__init__(*args, **kwargs)
        if generated_palette:
            self.fields['existing_color_palette'] = forms.ChoiceField(
                choices=[(color, color) for color in generated_palette],
                widget=forms.RadioSelect,
                required=False
            )



class UIRequirementForm(forms.ModelForm):
    FONT_CHOICES = [
        ('Arial', 'Arial'),
        ('Helvetica', 'Helvetica'),
        ('Times New Roman', 'Times New Roman'),
        ('Courier New', 'Courier New'),
        ('Verdana', 'Verdana'),
        ('Georgia', 'Georgia'),
        ('Palatino', 'Palatino'),
        ('Garamond', 'Garamond'),
        ('Bookman', 'Bookman'),
        ('Comic Sans MS', 'Comic Sans MS'),
        ('Trebuchet MS', 'Trebuchet MS'),
        ('Arial Black', 'Arial Black'),
        ('Impact', 'Impact'),
        ('Lobster', 'Lobster'),
        ('Roboto', 'Roboto'),
        ('Open Sans', 'Open Sans'),
        ('Lato', 'Lato'),
        ('Montserrat', 'Montserrat'),
        ('Raleway', 'Raleway'),
        ('Slabo 27px', 'Slabo 27px'),
    ]
    font = forms.ChoiceField(choices=FONT_CHOICES, widget=forms.RadioSelect)
    font_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = UIRequirement
        fields = ['font', 'font_color']


class TechnicalRequirementForm(forms.ModelForm):
    class Meta:
        model = TechnicalRequirement
        fields = ['development_framework', 'cms']


from .models import Bot

class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['llm']
        labels = {
            'llm': 'Choose the LLM for Code Generation',
        }



