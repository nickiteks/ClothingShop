# Generated by Django 3.2.5 on 2021-11-24 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
