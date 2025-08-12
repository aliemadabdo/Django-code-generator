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


class MarriedRecruit(models.Model):
    name = models.CharField(verbose_name="name")
    social_status = models.CharField(choices=[("", "--------"),("A", "أعزب"),("B", "متزوج")], verbose_name="social_status")
    phone_number = models.CharField(blank=True, null=True, unique=True, verbose_name="phone_number")
    start_date = models.DateTimeField(verbose_name="start_date")
    rec = models.CharField(max_length=100, blank=True, null=True, default="z", unique=True, help_text="x", choices=[("", "--------"),("A", "أعزب"),("B", "متزوج")], verbose_name="c")
    Gov = models.CharField(max_length=500, blank=True, null=True, default="دمنهور", unique=True, help_text="اختار المحافظة الحالية", choices=[("", "--------"),("A", "دمنهور"),("B", "الاسكندرية")], verbose_name="المحافظة")



class MarriedRecruit(models.Model):
    name = models.CharField(verbose_name="name")
    social_status = models.CharField(choices=[("", "--------"),("A", "أعزب"),("B", "متزوج")], verbose_name="social_status")
    phone_number = models.CharField(blank=True, null=True, unique=True, verbose_name="phone_number")
    start_date = models.DateTimeField(verbose_name="start_date")
    rec = models.CharField(max_length=100, blank=True, null=True, default="z", unique=True, help_text="x", choices=[("", "--------"),("A", "أعزب"),("B", "متزوج")], verbose_name="c")
    Gov = models.CharField(max_length=500, blank=True, null=True, default="دمنهور", unique=True, help_text="اختار المحافظة الحالية", choices=[("", "--------"),("A", "دمنهور"),("B", "الاسكندرية")], verbose_name="المحافظة")

