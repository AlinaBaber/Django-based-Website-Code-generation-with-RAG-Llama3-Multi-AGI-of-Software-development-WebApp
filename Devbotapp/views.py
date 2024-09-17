

from .DocGeneration import userrequirement_generate_docx
from .models import Question
from Devbotapp.Client.models import Client
from .forms import LogoUploadForm, ProjectTypeForm, DynamicQuestionForm, ProjectForm, UIRequirementForm
from colorthief import ColorThief
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import TechnicalRequirementForm
import logging
from .models import Project, UserResponse, UIRequirement, TechnicalRequirement
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project, UIRequirement, TechnicalRequirement
from django.utils.timezone import now
from django.http import JsonResponse
import io
from django.contrib.auth.decorators import login_required
from .forms import BotForm
from .models import Project, Bot
import os
import requests
import zipfile
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm
import os
import zipfile
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Project

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project, UIRequirement, TechnicalRequirement
from .serializers import UIRequirementSerializer, TechnicalRequirementSerializer

def welcome_view(request):
    if request.user.is_authenticated:
        print('request.user.is_authenticated',request.user.is_authenticated)
        return redirect('Devbotapp:home')
    return render(request, 'DevBotApp/welcome.html')
@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            request.session['project_id'] = project.id
            return redirect('Devbotapp:userrequirements', question_id=1)
    else:
        form = ProjectForm()

    return render(request, 'userrequirements/create_project.html', {'form': form})
@login_required
def select_project_type_view(request):
    if request.method == 'POST':
        form = ProjectTypeForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.name = "New Project"  # You can set this dynamically
            project.save()
            request.session['project_id'] = project.id
            return redirect('Devbotapp:userrequirements', question_id=1)
    else:
        form = ProjectTypeForm()

    return render(request, 'userrequirements/select_project_type.html', {'form': form})

@login_required
def userrequirements_view(request, question_id=1):
    project_id = request.session.get('project_id')
    if not project_id:
        return redirect('survey:create_project')

    project = Project.objects.get(id=project_id)
    client = Client.objects.get(user=request.user)

    general_questions = Question.objects.filter(project_type__isnull=True)

    if client.client_type == 'Simple':
        project_questions = Question.objects.filter(project_type=project.project_type)
        all_questions = list(general_questions) + list(project_questions)
    elif client.client_type == 'Professional':
        professional_questions = Question.objects.filter(project_type='Advanced Project Requirements')
        project_questions = Question.objects.filter(project_type=project.project_type)
        all_questions = list(general_questions)+list(professional_questions) + list(project_questions)
    else: # Business
        professional_questions = Question.objects.filter(project_type='Advanced Project Requirements')
        project_questions = Question.objects.filter(project_type=project.project_type)
        all_questions = list(general_questions) + list(professional_questions) + list(project_questions)

    if question_id <= len(all_questions):
        question = all_questions[question_id - 1]
    else:
        return redirect('Devbotapp:upload_logo')

    if request.method == 'POST':
        form = DynamicQuestionForm(question, request.POST)
        if form.is_valid():
            form.save_response(request.user, project)
            return redirect('Devbotapp:userrequirements', question_id=question_id + 1)
    else:
        form = DynamicQuestionForm(question)

    return render(request, 'userrequirements/question.html', {'form': form, 'question_id': question_id})

def home_view(request):
    return render(request, 'DevBotApp/home.html')


@login_required
def upload_logo_view(request):
    project_id = request.session.get('project_id')
    if not project_id:
        return HttpResponse("No project found in session.", status=400)

    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = LogoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save(commit=False)
            logo.project = project
            logo.save()
            palette = generate_color_palette(logo.image)
            return render(request, 'userrequirements/color_palette_generation.html', {'palette': palette})
    else:
        form = LogoUploadForm()

    return render(request, 'userrequirements/upload_logo.html', {'form': form})

def generate_color_palette(image_file):
    color_thief = ColorThief(image_file)
    palette = color_thief.get_palette(color_count=6)
    return palette

@login_required
def save_color_palette_view(request):
    if request.method == 'POST':
        color_choice = request.POST.get('color_choice')
        if color_choice == 'generated':
            palette = request.POST.getlist('generated_palette')
        else:
            palette = request.POST.getlist('custom_palette')

        request.session['color_palette'] = palette
        request.session['color_choice'] = color_choice

        project_id = request.session.get('project_id')
        if not project_id:
            return HttpResponse("No project found in session.", status=400)

        return redirect('Devbotapp:ui_requirements', project_id=project_id)
    else:
        return HttpResponse("Invalid request method.", status=405)

@login_required
def ui_requirements_view(request, project_id):
    project = Project.objects.get(id=project_id)
    palette = request.session.get('color_palette')
    color_choice = request.session.get('color_choice')

    if request.method == 'POST':
        form = UIRequirementForm(request.POST)
        if form.is_valid():
            ui_requirement, created = UIRequirement.objects.get_or_create(project=project)
            ui_requirement.font = form.cleaned_data['font']
            ui_requirement.font_color = form.cleaned_data['font_color']
            ui_requirement.color_palette = palette
            ui_requirement.color_choice = color_choice
            ui_requirement.save()
            return redirect('Devbotapp:technical_requirement', project_id=project.id)
    else:
        form = UIRequirementForm()

    return render(request, 'userrequirements/ui_requirements.html', {'form': form, 'project': project})




@login_required
def technical_requirement_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = TechnicalRequirementForm(request.POST)
        if form.is_valid():
            technical_requirement = form.save(commit=False)
            technical_requirement.user = request.user
            technical_requirement.project = project
            technical_requirement.save()
            return redirect('Devbotapp:project_details', project_id=project_id)
    else:
        form = TechnicalRequirementForm()

    return render(request, 'userrequirements/technical_requirement.html', {'form': form, 'project': project})



@login_required
def project_details_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_responses = UserResponse.objects.filter(project=project)
    ui_requirements = get_object_or_404(UIRequirement, project=project)
    technical_requirements = TechnicalRequirement.objects.filter(project=project)

    if request.method == 'POST':
        return redirect('Devbotapp:code_generation', project_id=project_id)

    # Ensure the color_palette is properly parsed if stored as JSON
    color_palette = ui_requirements.color_palette
    if isinstance(color_palette, str):
        import json
        color_palette = json.loads(color_palette)
        ui_requirements.color_palette = color_palette

    context = {
        'project': project,
        'user_responses': user_responses,
        'ui_requirements': ui_requirements,
        'technical_requirements': technical_requirements,
    }
    return render(request, 'userrequirements/project_details.html', context)



# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@login_required
def code_generation_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_responses = UserResponse.objects.filter(project=project)
    ui_requirements = get_object_or_404(UIRequirement, project=project)
    technical_requirements = TechnicalRequirement.objects.filter(project=project)

    context = {
        'project': project,
        'user_responses': user_responses,
        'ui_requirements': ui_requirements,
        'technical_requirements': technical_requirements,
    }
    return render(request, 'codegenerationprocess/code_generation.html', context)



@login_required
def start_code_generation(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_responses = UserResponse.objects.filter(project=project)
    ui_requirements = get_object_or_404(UIRequirement, project=project)
    technical_requirements = TechnicalRequirement.objects.filter(project=project)
    #bot = get_object_or_404(Bot, project=project)
    context = {
        'project': project,
        'user_responses': user_responses,
        'ui_requirements': ui_requirements,
        'technical_requirements': technical_requirements,
    }
    dataJSON={'color_palette': ui_requirements.color_palette,
          'font': ui_requirements.font,
          'font_color': ui_requirements.font_color,
    }
    log_messages = []

    def log(message):
        timestamp = now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {message}"
        log_messages.append(log_message)
        logger.info(log_message)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_log_message',
                'message': log_message
            }
        )

    if request.method == 'POST':
        channel_layer = get_channel_layer()
        group_name = f'code_generation_{project_id}'

        log("Starting document generation...")
        docx_file_path = userrequirement_generate_docx(context, project_id)
        log("User Requirement Document has been generated successfully.")

        base_url = settings.API_URLS['BASE_URL']
        endpoints = settings.API_URLS['ENDPOINTS']

        # Determine the correct software_developer endpoint based on the development framework
        development_framework = technical_requirements[0].development_framework if technical_requirements else None
        if development_framework == 'Django':
            software_developer_endpoint = endpoints['software_developer']   # Default endpoint
        elif development_framework == 'Static HTML':
            software_developer_endpoint = endpoints['software_developer_static']  # Default endpoint
        else:
            software_developer_endpoint = endpoints['software_developer']  # Default endpoint
        api_calls = [
            (endpoints['business_analysis'], {'file': docx_file_path, 'projectid': project_id}),
            (endpoints['software_architect'], {'projectid': project_id}),
            #(software_developer_endpoint, {'projectid': project_id}),
        ]
        #log(f"Selected software_developer endpoint: {software_developer_endpoint}")
        for endpoint, data in api_calls:
            log(f"Starting {endpoint.replace('_', ' ').title()} API...")
            url = f"{base_url}{endpoint}/"
            #for attempt in range(1):  # Try twice
            try:
                if 'file' in data:
                    log(f"Running {endpoint}")
                    with open(data['file'], 'rb') as f:
                        files = {'file': f}
                        response = requests.post(url, files=files, data={'projectid': project_id})
                else:
                    log(f"Running {endpoint}")
                    response = requests.post(url, json={'projectid': project_id})

                #log(f"Response status: {response.status_code}")
                #log(f"Response content: {response.content.}")

                if response.status_code == 200:
                    log(f"{response.json().get('Progress log', 'No log available')}")
                    break  # Break the loop if successful
                elif response.status_code == 202:
                    log(f"{response.json().get('Progress log', 'No log available')}")
                else:
                    log(f"Error calling {endpoint.replace('_', ' ').title()} API: {response.status_code}")
            except Exception as e:
                log(f"Exception calling {endpoint.replace('_', ' ').title()} API: {str(e)}")
        # Handle the third API call separately
        log(f"Starting {software_developer_endpoint.replace('_', ' ').title()}")
        software_developer_url = f"{base_url}{software_developer_endpoint}/"

        try:
            log(f"Running {software_developer_endpoint}")
            response = requests.post(software_developer_url, json={'projectid': project_id})

            if response.status_code == 200:
                progress_log = response.json().get('Progress log', 'No log available')
                log(progress_log)
                #ssbreak  # Break the loop if successful
            else:
                log(f"Error calling {software_developer_endpoint.replace('_', ' ').title()} API: {response.status_code}")
        except Exception as e:
            log(f"Exception calling {software_developer_endpoint.replace('_', ' ').title()} API: {str(e)}")

        log("All processes completed successfully.")
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'})


@login_required
def display_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_responses = UserResponse.objects.filter(project=project)
    ui_requirements = get_object_or_404(UIRequirement, project=project)
    technical_requirements = get_object_or_404(TechnicalRequirement, project=project)

    context = {
        'project': project,
        'user_responses': user_responses,
        'ui_requirements': ui_requirements,
        'technical_requirements': technical_requirements,
    }

    return render(request, 'codegenerationprocess/display_view.html', context)


@login_required
def email_change_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        request.user.email = email
        request.user.save()
        messages.success(request, 'Your email address has been updated.')
        return redirect('survey:home')
    return render(request, 'account/email_change.html')

def custom_logout_view(request):
    logout(request)
    return redirect('Devbotapp:welcome')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


@login_required
def build_by_chat_view(request):
    if not Client.objects.filter(user=request.user, client_type='Business').exists():
        return redirect('survey:home')
    return render(request, 'Devbotapp/build_by_chat.html')
@login_required
def display_generated_site(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project_dir = os.path.join(settings.MEDIA_ROOT, f'generated_sites/project_{project_id}')

    # Ensure the directory exists
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    # Fetch the zip file from the API
    base_url = settings.API_URLS['BASE_URL']
    endpoint = settings.API_URLS['ENDPOINTS']['download_project_zip']
    url = f"{base_url}{endpoint}/"

    try:
        response = requests.post(url, json={'projectid': project_id})
        response.raise_for_status()

        # Write the zip file to the project directory
        zip_path = os.path.join(project_dir, 'project_files.zip')
        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_dir)

        # Remove the zip file after extraction
        os.remove(zip_path)

    except requests.RequestException as e:
        raise Http404("Failed to fetch project files from the API.")

    # Load the main HTML file to display the site
    index_path = os.path.join(project_dir, 'index.html')
    if not os.path.exists(index_path):
        raise Http404("Index file not found in the project files.")

    with open(index_path, 'r') as file:
        html_content = file.read()

    return render(request, 'displaycode/displaysite.html', {'html_content': html_content, 'project': project})


@login_required
def download_project_zip(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    base_url = settings.API_URLS['BASE_URL']
    endpoint = settings.API_URLS['ENDPOINTS']['software_developer_code']
    url = f"{base_url}{endpoint}/"

    try:
        response = requests.post(url, json={'projectid': project_id}, stream=True)
        if response.status_code == 200:
            response_filename = f"project_{project_id}.zip"
            response_data = response.raw

            response = HttpResponse(response_data, content_type='application/zip')
            response['code_zip'] = f'attachment; filename={response_filename}'
            return response
        else:
            return HttpResponse(f"Error: Unable to download the zip file. Status code: {response.status_code}")
    except Exception as e:
        return HttpResponse(f"Exception: {str(e)}")


@login_required
def download_project_documents(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    base_url = settings.API_URLS['BASE_URL']
    endpoints = settings.API_URLS['ENDPOINTS']

    # Define the API calls for documents
    api_calls = [
        endpoints['business_analysis_document'],
        endpoints['software_architect_srs'],
        endpoints['software_architect_design'],
        endpoints['software_developer_codedoc']
    ]

    # Create a BytesIO buffer to hold the ZIP file
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        for endpoint in api_calls:
            url = f"{base_url}{endpoint}/"
            try:
                response = requests.post(url, json={'projectid': project_id})

                if response.status_code == 200:
                    document_content = response.json().get('Text', 'No content available')
                    document_name = f"{endpoint.replace('_', ' ').title()}.txt"

                    zf.writestr(document_name, document_content)
                else:
                    error_message = f"Error calling {endpoint.replace('_', ' ').title()} API: {response.status_code}"
                    zf.writestr(f"{endpoint.replace('_', ' ').title()}_Error.txt", error_message)
            except Exception as e:
                error_message = f"Exception calling {endpoint.replace('_', ' ').title()} API: {str(e)}"
                zf.writestr(f"{endpoint.replace('_', ' ').title()}_Exception.txt", error_message)

    # Prepare the HTTP response
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['documents'] = f'attachment; filename=project_{project_id}_documents.zip'

    return response

@api_view(['GET'])
def get_project_requirements(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

    ui_requirements = UIRequirement.objects.filter(project=project)
    technical_requirements = TechnicalRequirement.objects.filter(project=project)

    ui_serializer = UIRequirementSerializer(ui_requirements, many=True)
    technical_serializer = TechnicalRequirementSerializer(technical_requirements, many=True)

    ui_data = ui_serializer.data[0] if ui_serializer.data else {}
    tech_data = technical_serializer.data[0] if technical_serializer.data else {}

    data = {
        'font': ui_data.get('font', None),
        'font_color': ui_data.get('font_color', None),
        'color_palette': ui_data.get('color_palette', None),
        'framework': tech_data.get('development_framework', None),
        'cms': tech_data.get('cms', None),
    }

    return Response(data)

