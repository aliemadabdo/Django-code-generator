from django.db import models

# Create your models here.

class ModelField(models.Model):
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)
    is_foreign_key = models.BooleanField(default=False)
    related_model = models.CharField(max_length=100, blank=True, null=True)
    choices = models.TextField(blank=True, null=True)  # JSON format
    choices_from_database = models.TextField(blank=True, null=True)  # Model.objects.all()
    max_length = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=False)
    unique = models.BooleanField(default=False)
    blank = models.BooleanField(default=False)
    null = models.BooleanField(default=False)
    default = models.CharField(max_length=100, blank=True, null=True)
    verbose_name = models.CharField(max_length=100, blank=True, null=True)
    help_text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.field_name


