# Generated by Django 4.2.1 on 2023-05-29 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default='Default Username', max_length=50),
        ),
    ]