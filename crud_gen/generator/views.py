from django.shortcuts import render

from generator.configs import APP_NAME
from generator.forms import CreateAppForm, modelForm, ModelFieldForm
from generator.helpers import *
from generator.models import ModelField

# Create your views here.

def home(request):
    return render(request, 'generator/home.html')

def about(request):
    return render(request, 'generator/about.html')

def contact(request):
    return render(request, 'generator/contact.html')

def add_model(request):
    if request.method == 'POST':
        form = modelForm(request.POST)
        if form.is_valid():
            # Process the form data and create the model
            model_name = form.cleaned_data['model_name']
            model_fields = form.cleaned_data['model_fields']
            print(f"Creating model: {model_name} with fields: {[field.field_name for field in model_fields]}")
            # i need to print the internal data of fields inside the model_fields
            for field in model_fields:
                print(f"Field Name: {field.field_name}, Type: {field.field_type}, Is Foreign Key: {field.is_foreign_key}, Related Model: {field.related_model}, blank: {field.blank}, null: {field.null}, default: {field.default}, verbose_name: {field.verbose_name}, help_text: {field.help_text}")
                # You can also access other attributes if needed

            CreateModel(APP_NAME, model_name, model_fields)
            
            # Redirect or render a success message
            return render(request, 'generator/add_model.html', {'model_name': model_name})
    else:
        # Render the form for adding a model
        form = modelForm()
        return render(request, 'generator/add_model.html', {'form': form})
    
    return render(request, 'generator/add_model.html')

def add_model_field(request):
    if request.method == 'POST':
        form = ModelFieldForm(request.POST)
        if form.is_valid():
            # Process the form data and create the model field
            field_data = form.cleaned_data

            field_name = field_data['field_name']
            field_type = field_data['field_type']
            is_foreign_key = field_data['field_is_foreign_key']
            related_model = field_data.get('field_related_model')
            choices = field_data.get('field_choices')
            choices_from_db = field_data.get('field_choices_from_database')
            max_length = field_data.get('field_max_length')
            required = field_data.get('field_required', False)
            unique = field_data.get('field_unique', False)
            blank = field_data.get('field_blank', False)
            null = field_data.get('field_null', False)
            default = field_data.get('field_default')
            verbose_name = field_data.get('field_verbose_name', field_name)
            help_text = field_data.get('field_help_text', '')
            options = field_data.get('field_options')


            modelField = ModelField.objects.create(
                field_name=field_name,
                field_type=field_type,
                is_foreign_key=is_foreign_key,
                related_model=related_model,
                choices=choices,
                max_length=max_length,
                required=required,
                unique=unique,
                blank=blank,
                null=null,
                default=default,
                verbose_name=verbose_name,
                help_text=help_text
            )

            modelField.save()
            # Here you would typically save the field to the database or use it as needed
            return render(request, 'generator/success.html', {'success': True, 'field_name': field_name})
    else:
        # Render the form for adding a model field
        form = ModelFieldForm()
        return render(request, 'generator/add_model_field.html', {'form': form})

def create_crud_app(request):
    if request.method == 'POST':
        form = CreateAppForm(request.POST)
        if form.is_valid():
            model_name = form.cleaned_data['model_name']
            app_title = form.cleaned_data['app_title']

            create_forms(model_name)
            create_urls(model_name)
            create_views(model_name)
            create_templates(model_name, app_title)

        return render(request, 'generator/success_app.html', {'success': True, 'app_title': app_title})
        
    else:
        form = CreateAppForm()
        return render(request, 'generator/create_crud_app.html', {'form': form})
