# Generated by Django 5.0.7 on 2024-07-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptions',
            options={'permissions': [('basic', 'Basic Permissions'), ('pro', 'Pro Permissions'), ('advance', 'Advanced Permissions'), ('basic plus', 'Basic Plus Permissions')]},
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='permissions',
            field=models.ManyToManyField(limit_choices_to={'codename__in': ['basic', 'pro', 'advance', 'basic plus'], 'content_type__app_label': 'subscription'}, to='auth.permission'),
        ),
    ]
