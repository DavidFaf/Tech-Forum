# Generated by Django 4.2.2 on 2023-06-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]