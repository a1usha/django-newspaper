# Generated by Django 3.1.3 on 2021-05-16 05:32

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210516_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetask',
            name='image',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='texttask',
            name='author',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
