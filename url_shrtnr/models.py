from django.db import models


class Url(models.Model):
    full_url = models.CharField(max_length=255, default="", unique=True)
    shortened_url = models.CharField(max_length=255, default="")
