# Generated by Django 5.0.2 on 2024-04-24 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0005_pet_avatar_alter_pet_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
