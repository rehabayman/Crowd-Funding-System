# Generated by Django 2.1 on 2020-04-21 14:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
