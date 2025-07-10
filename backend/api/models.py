from django.db import models

class Style(models.Model):
    name = models.CharField(max_length=100, unique=True)
    instruction = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Context(models.Model):
    name = models.CharField(max_length=100, unique=True)
    instruction = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name