# Generated by Django 5.0.2 on 2024-04-27 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalapp', '0003_alter_question_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='functionalapp.answer'),
        ),
    ]
