import os
import subprocess
import time
from generator.configs import *


def snack_case(name):
    """
    Convert a string to snake_case.
    replace capetalized letters with lowercase and underscores except for the first letter.
    example: "MyModel" -> "my_model"
    """
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
    
def build_field_code(field):
    """
    field: ModelField instance from DB
    Returns the code string for that field.
    """
    # Use attributes instead of dict keys
    field_name = field.field_name
    field_type = field.field_type
    is_fk = field.is_foreign_key
    related_model = field.related_model
    verbose_name = field.verbose_name or field_name
    max_length = field.max_length
    
    extra_args = []

    # Common options for all fields
    if field.blank:
        extra_args.append("blank=True")
    if field.null:
        extra_args.append("null=True")
    if field.default:
        extra_args.append(f'default="{field.default}"')
    # if field.required:
    #     extra_args.append("blank=False")
    if field.unique:
        extra_args.append("unique=True")
    if field.help_text:
        extra_args.append(f'help_text="{field.help_text}"')
    if field.choices:
        extra_args.append(f'choices={field.choices}')
    elif field.choices_from_database:
        extra_args.append(f'choices={field.choices_from_database}.objects.all()')
    

    if getattr(field, 'db_index', False):
        extra_args.append("db_index=True")

    # Add verbose name
    extra_args.append(f'verbose_name="{verbose_name}"')

    # Build FK or normal field
    if is_fk and related_model:
        code = f"{field_name} = models.ForeignKey({related_model}, on_delete=models.SET_NULL, {', '.join(extra_args)})"
        print(f"Field code for {field_name}: {code}")
    else:
        if field_type == "CharField" and max_length:
            extra_args.insert(0, f"max_length={max_length}")
        code = f"{field_name} = models.{field_type}({', '.join(extra_args)})"

    return code

def CreateModel(app_name, model_name, model_fields):
    """
    model_fields: list of dicts (from ModelFieldForm.cleaned_data)
    """
    # app_path = os.path.join(PROJECT_URL, app_name)
    models_file_path = os.path.join(TARGET_URL, 'models.py')

    # Build all field lines
    fields_code = ""
    for field in model_fields:
        fields_code += f"    {build_field_code(field)}\n"

    model_code = f"\n\nclass {model_name}(models.Model):\n{fields_code}\n"

    # Create or append
    if not os.path.exists(models_file_path):
        with open(models_file_path, 'w', encoding='utf-8') as f:
            f.write("from django.db import models\n")
            f.write(model_code)
    else:
        with open(models_file_path, 'a', encoding='utf-8') as f:
            f.write(model_code)
    f.close()

    # Run migrations
    time.sleep(2)  # small delay
    subprocess.run(['python', 'manage.py', 'makemigrations', app_name], cwd=PROJECT_URL)
    subprocess.run(['python', 'manage.py', 'migrate'], cwd=PROJECT_URL)
    time.sleep(2)  # small delay

    register_model_in_admin(model_name, os.path.join(TARGET_URL, 'admin.py'))

def register_model_in_admin(model_name, admin_file_path):
    """
    Append an @admin.register block for the given model to admin.py.
    Does nothing if the model is already registered.
    """
    try:
        block = f"\n@admin.register({model_name})\nclass {model_name}Admin(admin.ModelAdmin):\n    pass\n"

        with open(admin_file_path, "a", encoding="utf-8") as f:
            f.write(block)

        print(f"{model_name} successfully registered in {admin_file_path}.")
    except FileNotFoundError:
        print(f"File {admin_file_path} not found.")

def create_forms(model_name):
    # create the form based on the model name
    form_code = f"""
from django import forms
from .models import {model_name}
class {model_name}Form(forms.ModelForm):
    class Meta:
        model = {model_name}
        fields = '__all__'
        """
    forms_file_path = os.path.join(TARGET_URL, 'forms.py')
    with open(forms_file_path, 'a', encoding='utf-8') as f:
        f.write(form_code)

def create_urls(model_name):
    model_name_snake = snack_case(model_name)
    # here we will add for urls for the add, search, edit and delete views
    # but the app process is a bit complicated 
    # if its a new file we will add code and if it already created we will add another 
    # also the position of the add code to the already created one will be add before the last ] in the file urls.py

    urls_code_if_empty = f"""
from django.urls import path, include
from .views import *
app_name = '{APP_NAME}'
urlpatterns = [
    # Define your app's URLs here

    path('add_{model_name_snake}/', add_{model_name_snake}, name='add_{model_name_snake}'),
    path('search_{model_name_snake}/', search_{model_name_snake}, name='search_{model_name_snake}'),
    path('edit_{model_name_snake}/<int:id>/', edit_{model_name_snake}, name='edit_{model_name_snake}'),
    path('delete_{model_name_snake}/<int:id>/', delete_{model_name_snake}, name='delete_{model_name_snake}'),
    
]
        """
    urls_code_if_found = f"""
path('add_{model_name_snake}/', add_{model_name_snake}, name='add_{model_name_snake}'),
path('search_{model_name_snake}/', search_{model_name_snake}, name='search_{model_name_snake}'),
path('edit_{model_name_snake}/<int:id>/', edit_{model_name_snake}, name='edit_{model_name_snake}'),
path('delete_{model_name_snake}/<int:id>/', delete_{model_name_snake}, name='delete_{model_name_snake}'),

        """
    urls_file_path = os.path.join(TARGET_URL, 'urls.py')
    if not os.path.exists(urls_file_path):
        with open(urls_file_path, 'w', encoding='utf-8') as f:
            f.write(urls_code_if_empty)
    else:
        with open(urls_file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            if urls_code_if_found not in content:
                # Find the last closing bracket and insert before it
                insert_position = content.rfind(']')
                if insert_position != -1:
                    new_content = content[:insert_position] + urls_code_if_found + content[insert_position:]
                    f.seek(0)
                    f.write(new_content)
                    f.truncate()

def create_add_view(model_name):
    model_name_snake = snack_case(model_name)
    # a basic add view for the model that handels the form and save the data to the database
    add_view_code = f"""
def add_{model_name_snake}(request):
    from .forms import {model_name}Form
    if request.method == 'POST':
        form = {model_name}Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, '{APP_NAME}/add_{model_name_snake}.html', {{'success': True}})
    else:
        form = {model_name}Form()
    return render(request, '{APP_NAME}/success.html', {{'var': add, 'model_name': '{model_name}'}})
    """
    views_file_path = os.path.join(TARGET_URL, 'views.py')
    with open(views_file_path, 'a', encoding='utf-8') as f:
        f.write(add_view_code)


def create_search_view(model_name):
    model_name_snake = snack_case(model_name)
    # a basic search view for the model that handels the form and filters the data from the database
    # it will show all the data if no search query is provided
    # next phase we will add order by feature and choose which columns to show
    pass

def create_edit_view(model_name):
    model_name_snake = snack_case(model_name)
    # a basic edit view for the model that handels the form and update the data to the database
    edit_view_code = f"""
def edit_{model_name_snake}(request, id):
    from .models import {model_name}
    from .forms import {model_name}Form
    obj = {model_name}.objects.get(id=id)
    if request.method == 'POST':
        form = {model_name}Form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return render(request, '{APP_NAME}/success.html', {{'var': edit, 'model_name': '{model_name}'}})
    else:
        form = {model_name}Form(instance=obj)
    return render(request, '{APP_NAME}/edit_{model_name_snake}.html', {{'form': form}})
    """
    views_file_path = os.path.join(TARGET_URL, 'views.py')
    with open(views_file_path, 'a', encoding='utf-8') as f:
        f.write(edit_view_code)

def create_delete_view(model_name):
    model_name_snake = snack_case(model_name)
    # a basic delete view for the model that deletes the data from the database based on the id provided in the url
    delete_view_code = f"""
def delete_{model_name_snake}(request, id):
    from .models import {model_name}
    obj = {model_name}.objects.get(id=id)
    obj.delete()
    return render(request, '{APP_NAME}/delete_{model_name_snake}.html', {{'success': True}})
    """
    views_file_path = os.path.join(TARGET_URL, 'views.py')
    with open(views_file_path, 'a', encoding='utf-8') as f:
        f.write(delete_view_code)

def create_views(model_name):
    model_name_snake = snack_case(model_name)
    create_add_view(model_name)
    create_search_view(model_name)
    create_edit_view(model_name)
    create_delete_view(model_name)

def create_templates(model_name, app_title):
    model_name_snake = snack_case(model_name)
    pass