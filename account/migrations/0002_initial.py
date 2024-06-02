# Generated by Django 4.2.11 on 2024-04-13 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.faculty', verbose_name='faculty'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.field', verbose_name='field'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='taught_courses',
            field=models.ManyToManyField(related_name='taught_courses', to='department.course', verbose_name='taught courses'),
        ),
        migrations.AddField(
            model_name='student',
            name='advisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.teacher', verbose_name='advisor'),
        ),
        migrations.AddField(
            model_name='student',
            name='entry_term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.term', verbose_name='entry term'),
        ),
        migrations.AddField(
            model_name='student',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.faculty', verbose_name='faculty'),
        ),
        migrations.AddField(
            model_name='student',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.field', verbose_name='field'),
        ),
        migrations.AddField(
            model_name='student',
            name='in_progress_courses',
            field=models.ManyToManyField(related_name='in_progress_courses', to='department.course', verbose_name='in progress courses'),
        ),
        migrations.AddField(
            model_name='student',
            name='passed_courses',
            field=models.ManyToManyField(related_name='passed_courses', to='department.course', verbose_name='passed courses'),
        ),
        migrations.AddField(
            model_name='educationalassistant',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.faculty', verbose_name='faculty'),
        ),
        migrations.AddField(
            model_name='educationalassistant',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='department.field', verbose_name='field'),
        ),
    ]
