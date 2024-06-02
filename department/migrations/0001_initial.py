# Generated by Django 4.2.11 on 2024-04-13 17:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('units', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], verbose_name='units')),
                ('type', models.CharField(choices=[('optional', 'Optional'), ('basic', 'Basic'), ('general', 'General'), ('specialized', 'Specialized'), ('other', 'Other')], max_length=100, verbose_name='type')),
                ('corequisites_courses', models.ManyToManyField(blank=True, related_name='corequisites', to='department.course', verbose_name='corequisites courses')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'faculty',
                'verbose_name_plural': 'faculties',
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('class_start', models.DateTimeField(verbose_name='class start')),
                ('class_end', models.DateTimeField(verbose_name='class end')),
                ('enrollment_start', models.DateTimeField(verbose_name='enrollment start')),
                ('enrollment_end', models.DateTimeField(verbose_name='enrollment end')),
                ('amend_start', models.DateTimeField(verbose_name='amend start')),
                ('amend_end', models.DateTimeField(verbose_name='amend end')),
                ('emergency_drop_end', models.DateTimeField(verbose_name='emergency drop end')),
                ('exam_start', models.DateTimeField(verbose_name='exam start')),
                ('term_end', models.DateTimeField(verbose_name='term end')),
            ],
            options={
                'verbose_name': 'term',
                'verbose_name_plural': 'terms',
            },
        ),
        migrations.CreateModel(
            name='TermCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('exam_date', models.DateTimeField(blank=True, null=True)),
                ('capacity', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.course')),
                ('exam_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.faculty')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.teacher')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.term')),
            ],
            options={
                'verbose_name': 'term course',
                'verbose_name_plural': 'term courses',
            },
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_status', models.CharField(choices=[('started', 'Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], max_length=20)),
                ('student_score', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(20.0)])),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.student')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.term')),
            ],
            options={
                'verbose_name': 'student course',
                'verbose_name_plural': 'student courses',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('academic_department', models.CharField(max_length=20)),
                ('credit_numbers', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(200)])),
                ('grade', models.CharField(choices=[('bachelor', 'Bachelor'), ('master', 'Master'), ('doctorate', 'Doctorate')], max_length=20)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.faculty')),
            ],
            options={
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='offering_faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.faculty', verbose_name='offering faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites_courses',
            field=models.ManyToManyField(blank=True, related_name='prerequisites', to='department.course', verbose_name='prerequisites courses'),
        ),
    ]
