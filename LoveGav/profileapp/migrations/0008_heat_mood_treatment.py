# Generated by Django 5.0.2 on 2024-05-06 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0007_alter_pet_avatar_alter_pet_passport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soreness', models.CharField(blank=True, max_length=50, null=True)),
                ('data', models.DateField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood_day', models.CharField(choices=[('slug', 'sluggish'), ('rest', 'restless'), ('aggr', 'aggressive'), ('norm', 'normal'), ('play', 'playful'), ('exc', 'excellent')], max_length=4)),
                ('data', models.DateField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('data', models.DateField()),
                ('data_next', models.DateField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileapp.pet')),
            ],
        ),
    ]
