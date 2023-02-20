# Generated by Django 4.1.5 on 2023-02-20 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deficiency_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('date_fulfilled', models.DateField(blank=True, default=None, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('name', models.CharField(default=None, max_length=100)),
                ('category', models.CharField(default=None, max_length=100)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_by', to='school.employeeprofile')),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processed_by', to='school.employeeprofile')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_with_deficiency', to='school.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='FinanceDeficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('deficiency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deficiency.deficiency')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentDeficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=100)),
                ('deficiency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deficiency.deficiency')),
            ],
        ),
    ]