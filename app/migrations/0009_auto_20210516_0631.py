# Generated by Django 3.1.3 on 2021-05-16 06:31

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210516_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='page_size',
            field=models.CharField(choices=[('berliner', 'Berliner - 315 x 470 mm (12.4" x 18.5")'), ('broadsheet', 'Broadsheet - 600 x 750 mm (23.5" x 29.5")'), ('tabloid', 'Tabloid - 280 x 430 mm (11.0" x 16.9")')], default='berliner', max_length=100),
        ),
        migrations.AlterField(
            model_name='texttask',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
