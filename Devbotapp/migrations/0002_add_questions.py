from django.db import migrations, models
import json
import os

def load_questions(apps, schema_editor):
    ProjectType = apps.get_model('Devbotapp', 'ProjectType')
    Question = apps.get_model('Devbotapp', 'Question')
    Option = apps.get_model('Devbotapp', 'Option')

    # Get the path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), '..', 'questions.json')

    # Load questions from JSON file
    with open(json_path) as f:
        data = json.load(f)

    # Add project types and questions
    for item in data['questions']:
        project_type_name = item['project']
        project_type = None
        if project_type_name != "General":
            project_type, created = ProjectType.objects.get_or_create(name=project_type_name)

        for question_data in item['questions']:
            question = Question.objects.create(
                text=question_data['question'],
                question_type=question_data['QUESTION_TYPE'],
                project_type=project_type
            )
            for option_text in question_data['options']:
                Option.objects.create(question=question, text=option_text)

class Migration(migrations.Migration):

    dependencies = [
        ('Devbotapp', '0001_initial'),  # Ensure this matches the last migration file
    ]

    operations = [
        migrations.RunPython(load_questions),
    ]
