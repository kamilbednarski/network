# Generated by Django 3.1.3 on 2021-01-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20210104_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followed_by_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_count',
            field=models.IntegerField(default=0),
        ),
    ]
