# Generated by Django 5.0.2 on 2024-05-10 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('functionalapp', '0007_alter_answer_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playground',
            options={'ordering': ['town']},
        ),
    ]
