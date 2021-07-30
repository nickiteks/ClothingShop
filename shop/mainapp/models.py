from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    title = models.CharField(max_length=255,verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField()