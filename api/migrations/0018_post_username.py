# Generated by Django 4.2.1 on 2023-06-04 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_post_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='username',
            field=models.CharField(blank=True, default='Default Username', max_length=50, null=True),
        ),
    ]