# Generated by Django 3.1.3 on 2021-01-06 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210106_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='friend_id',
            new_name='users_friend',
        ),
    ]
