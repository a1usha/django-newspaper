# Generated by Django 3.1.3 on 2021-05-16 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210516_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articletask',
            name='article',
        ),
        migrations.AddField(
            model_name='article',
            name='articletask',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.articletask'),
        ),
        migrations.AlterField(
            model_name='newspaper',
            name='page_size',
            field=models.CharField(choices=[('broadsheet', 'Broadsheet - 600 x 750 mm (23.5" x 29.5")'), ('berliner', 'Berliner - 315 x 470 mm (12.4" x 18.5")'), ('tabloid', 'Tabloid - 280 x 430 mm (11.0" x 16.9")')], default='berliner', max_length=100),
        ),
    ]