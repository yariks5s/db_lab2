# Generated by Django 4.2.1 on 2023-05-07 23:08

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='online course', max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('distributor_name', models.CharField(default='Unknown', max_length=100)),
                ('pub_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateField(auto_now_add=True)),
                ('progress', models.PositiveSmallIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DBLab2.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Lesson title', max_length=200)),
                ('content', models.TextField()),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DBLab2.course')),
            ],
        ),
        migrations.CreateModel(
            name='QuestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, null=True)),
                ('answer', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='noname', max_length=30)),
                ('first_name', models.CharField(default='john', max_length=30)),
                ('last_name', models.CharField(default='doe', max_length=30)),
                ('social_link', models.URLField(default='')),
                ('dob', models.DateField(null=True)),
                ('is_instructor', models.BooleanField(default=False)),
                ('courses', models.ManyToManyField(related_name='learners', through='DBLab2.Enrollment', to='DBLab2.course')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LessonsLearnerRelations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField()),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DBLab2.user')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DBLab2.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DBLab2.questmodel'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DBLab2.user'),
        ),
        migrations.CreateModel(
            name='CoursesLearnerRelations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DBLab2.course')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DBLab2.user')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='enrollments',
            field=models.ManyToManyField(related_name='enrollments', through='DBLab2.Enrollment', to='DBLab2.user'),
        ),
    ]
