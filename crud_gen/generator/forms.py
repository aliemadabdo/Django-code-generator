from django import forms

from generator.models import ModelField


class modelForm(forms.Form):    # This form is used to create a model with the specified fields
    model_name = forms.CharField(label='Model Name', max_length=100)

    # a select multiple choice field to select the fields of the model
    # the fields should be as dropdown options
    # the options should be the fields defined in ModelFieldForm stored in the database
    # the user can select multiple fields to create the model
    model_fields = forms.ModelMultipleChoiceField(
        queryset=ModelField.objects.all(),
        label='Model Fields',
        widget=forms.CheckboxSelectMultiple,
        help_text='Select the fields to include in the model. You can create fields using the ModelFieldForm.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_fields'].queryset = ModelField.objects.all()

    def clean_model_name(self):
        model_name = self.cleaned_data.get('model_name')
        if not model_name:
            raise forms.ValidationError('Model name is required.')
        return model_name
    
class ModelFieldForm(forms.Form):
    # This form is used to create get the structure of the model fields then use it to generate the model
    field_name = forms.CharField(label='Field Name', max_length=100)
    field_type = forms.ChoiceField(
        label='Field Type',
        choices=[
            ('CharField', 'CharField'),
            ('IntegerField', 'IntegerField'),
            ('DateTimeField', 'DateTimeField'),
            ('BooleanField', 'BooleanField'),
            ('SearchField', 'SearchField'),
            ('ForeignKey', 'ForeignKey'),
            ('ManyToManyField', 'ManyToManyField'),
            ('OneToOneField', 'OneToOneField'),
            ('TextField', 'TextField'),
            ('EmailField', 'EmailField'),
            ('URLField', 'URLField'),
            ('FileField', 'FileField'),
            ('ImageField', 'ImageField'),
            # Add more field types as needed
        ]
    )
    field_is_foreign_key = forms.BooleanField(
        label='Is Foreign Key',
        required=False,
        help_text='Check if this field is a foreign key'
    )
    field_related_model = forms.CharField(
        label='Related Model',
        max_length=100,
        required=False,
        help_text='Optional, only if this field is a foreign key'
    )
    field_choices = forms.CharField(
        label='Choices',
        max_length=500,
        required=False,
        help_text='Optional choices for the field in JSON format, e.g. [{"value": "1", "label": "Choice 1"}]'
    )
    field_choices_from_database = forms.CharField(
        label='Choices from Database',
        max_length=500,
        required=False,
        help_text='Optional choices from database with the model name ex:Model.objects.all()'
    )
    field_max_length = forms.IntegerField(
        label='Max Length',
        required=False,
        help_text='Optional, only for CharField'
    )
    field_required = forms.BooleanField(
        label='Required',
        required=False,
        help_text='Check if this field is required'
    )
    field_unique = forms.BooleanField(
        label='Unique',
        required=False,
        help_text='Check if this field should be unique'
    )
    field_blank = forms.BooleanField(
        label='Blank',
        required=False,
        help_text='Check if this field can be blank'
    )
    field_null = forms.BooleanField(
        label='Null',
        required=False,
        help_text='Check if this field can be null'
    )   
    field_default = forms.CharField(
        label='Default Value',
        max_length=100,
        required=False,
        help_text='Optional default value for the field'
    )
    field_help_text = forms.CharField(
        label='Help Text',
        max_length=200,
        required=False,
        help_text='Optional help text for the field'
    )
    field_verbose_name = forms.CharField(
        label='Verbose Name',
        max_length=100,
        required=False,
        help_text='Optional verbose name for the field'
    )
    field_options = forms.CharField(
        label='Field Options',
        max_length=500,
        required=False,
        help_text='Optional field options in JSON format, e.g. {"max_length": 255}'
    )