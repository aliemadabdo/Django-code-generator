import os
import subprocess
import time
from generator.configs import PROJECT_URL, TARGET_URL


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
