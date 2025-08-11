from django.contrib import admin 
# Register your models here.

from generator.models import *

@admin.register(ModelField)
class ModelFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'field_type', 'is_foreign_key', 'related_model', 'choices', 'max_length', 'required', 'unique', 'blank', 'null', 'default', 'verbose_name', 'help_text')
    search_fields = ('field_name', 'field_type')
    list_filter = ('is_foreign_key', 'required', 'unique')
    ordering = ('field_name',)

