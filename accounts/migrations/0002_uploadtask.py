# Generated by Django 4.1.5 on 2023-05-04 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('csv_generated', models.BooleanField(default=False)),
                ('csv_filename', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
    ]
