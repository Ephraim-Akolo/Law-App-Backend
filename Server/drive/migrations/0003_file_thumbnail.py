# Generated by Django 3.2.24 on 2024-03-18 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0002_auto_20240318_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='thumbnail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='drive.thumbnail'),
        ),
    ]
