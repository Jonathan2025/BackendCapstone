# Generated by Django 4.2.1 on 2023-05-26 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_username_comment_userid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]