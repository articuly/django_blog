# Generated by Django 2.2.10 on 2020-03-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('course', '0002_auto_20200323_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
