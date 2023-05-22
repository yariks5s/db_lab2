import django
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(models.Model):
    username = models.CharField(null=False, max_length=30, default='noname')
    first_name = models.CharField(null=False, max_length=30, default='noname')
    last_name = models.CharField(null=False, max_length=30, default='noname')
    social_link = models.URLField(default="", max_length=200)
    email = models.EmailField(null=False, max_length=254, default='noemail')
    is_instructor = models.BooleanField(default=False)
    courses = models.ManyToManyField('Course', through='Enrollment', related_name='learners')

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default='online course', )
    description = models.CharField(max_length=500, )
    distributor_name = models.CharField(null=False, max_length=100, default='Unknown', )
    pub_date = models.DateField(default=django.utils.timezone.now, )
    enrollments = models.ManyToManyField(User, through='Enrollment', related_name='enrollments')

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=django.utils.timezone.now)
    progress = models.PositiveSmallIntegerField(default=0)


# Model for quiz
class QuestModel(models.Model):
    question = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.question

# Lesson
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson title")
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    questions = models.ForeignKey(QuestModel, null=True, on_delete=models.CASCADE)

class CoursesLearnerRelations(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class LessonsLearnerRelations(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    percentage = models.FloatField()

