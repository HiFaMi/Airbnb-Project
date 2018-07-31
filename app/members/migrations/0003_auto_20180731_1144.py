# Generated by Django 2.0.7 on 2018-07-31 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_likes_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_facebook_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_host',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
