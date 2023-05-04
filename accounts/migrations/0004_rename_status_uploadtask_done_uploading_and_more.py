# Generated by Django 4.1.5 on 2023-05-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_uploadtask_job_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadtask',
            old_name='status',
            new_name='done_uploading',
        ),
        migrations.AddField(
            model_name='uploadtask',
            name='failed',
            field=models.BooleanField(default=False),
        ),
    ]
