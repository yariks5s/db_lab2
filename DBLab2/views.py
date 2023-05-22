from django.contrib.auth import login
from django.http import HttpResponse
import datetime
from . import models
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from DBLab2.forms import NewLearnerForm, CourseForm, EnrollmentForm


def hello_world(request):
    return HttpResponse('Hello, World!')

class RegisterView(View):
    def registration_request(request):
        if request.method == "POST":
            form = NewLearnerForm(request.POST)
            if form.is_valid():
                learner = form.save()
                learn = models.User.objects.create(username=learner.username, first_name=learner.first_name,
                                            last_name=learner.last_name, social_link=learner.social_link,
                                            is_instructor=True, email=learner.email)
                return redirect("index")
        form = NewLearnerForm()
        return render(request=request, template_name="DBLab2/UserInput.html", context={"register_form": form})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = CourseForm()
    return render(request, 'DBLab2/CourseInput.html', {'form': form})

class CourseView(View):
    def get(self, request):
        if request.method == 'GET':
            courses = Course.objects.all()
            if courses is None:
                return HttpResponse(status=404, content="Course not found")
            else:
                context = {
                    'course_list': courses
                }
                return render(request, 'courses/index.html', context)
        else:
            return HttpResponse("Request processed")

    def post(self, request):
        pass

def create_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = EnrollmentForm()
    return render(request, 'DBLab2/EnrollmentInput.html', {'form': form})


class EnrollView(View):

    # @login_required
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('pkc')
        user_id = request.user.id
        # We get URL parameter pk from keyword argument list as course_id
        try:
            temp_course = Course.objects.get(pk=course_id)
            temp_user = User.objects.get(pk=user_id-5)
            new_enrollment = Enrollment()
            new_enrollment.course = temp_course
            new_enrollment.learner = temp_user

            new_enrollment.save()
            return redirect("courses:course_details", course_id)
        except:
            raise InterruptedError("There is an unexpected error. Please, try again.")

class CourseDetailsView(View):

    # Handles get request
    def get(self, request, *args, **kwargs):
        context = {}
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        user_id = request.user.id - 5
        try:
            course = Course.objects.get(pk=course_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            instructors = course.instructors.all()
            users = User.objects.get(pk=user_id)
            exists = Enrollment.objects.filter(course_id=course_id, learner_id=user_id)
            context = {'course': course,
                       'course_id': course_id,
                       'lessons': lessons,
                       'instructors': instructors,
                       'users': users,
                       'exists': exists,
                       }
            return render(request, 'courses/coursepage.html', context)
        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")

class CourseProgressView(View):
    # Handles get request
    def get(self, request, *args, **kwargs):
        context = {}
        done_lessons = []
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        user_id = request.user.id - 5
        try:
            course = Course.objects.get(pk=course_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            for i in range(len(lessons)):
                if LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=user_id).exists():
                    done_lessons.append(LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=request.user.id-5))
                    print(done_lessons)
            instructors = course.instructors.all()
            users = User.objects.get(pk=user_id)
            exists = Enrollment.objects.filter(course_id=course_id, learner_id=user_id)
            num_of_lessons = len(lessons)
            num_of_done_lessons = len(done_lessons)
            percent_of_done_lessons = (num_of_done_lessons / num_of_lessons * 100).__round__(1)
            show_list = ['Done', 'Not done']
            progress_list = [percent_of_done_lessons, 100-percent_of_done_lessons]
            context = {'course': course,
                       'course_id': course_id,
                       'lessons': lessons,
                       'done_lessons': done_lessons,
                       'instructors': instructors,
                       'users': users,
                       'exists': exists,
                       'num_of_lessons': num_of_lessons,
                       'num_of_done_lessons': num_of_done_lessons,
                       'percent_of_done_lessons': percent_of_done_lessons,
                       'show_list': show_list,
                       'progress_list': progress_list,
                       }
            return render(request, 'courses/courseprogress.html', context)
        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")

class LessonView(View):
    # Handles get request
    def get(self, request, *args, **kwargs):
        done_lessons = []
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        lesson_id = kwargs.get('pkl')
        # print(request.POST['option'])
        try:
            user_id = request.user.id - 5
            learner = User.objects.get(id=request.user.id - 5)
            course = Course.objects.get(pk=course_id)
            lesson = Lesson.objects.get(pk=lesson_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            quiz = QuestModel.objects.get(pk=lesson.questions_id)
            is_done = LessonsLearnerRelations.objects.filter(learner=learner, lesson=lesson).exists()
            num_of_lessons = len(lessons)
            for i in range(len(lessons)):
                if LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=user_id).exists():
                    done_lessons.append(LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=request.user.id-5))
                    print(done_lessons)
            num_of_done_lessons = len(done_lessons)
            percent_of_done_lessons = (num_of_done_lessons / num_of_lessons * 100).__round__(1)
            print(percent_of_done_lessons)
            if percent_of_done_lessons == 100.0 and not CoursesLearnerRelations.objects.filter(course_id=course_id, learner_id=user_id).exists():
                rel = CoursesLearnerRelations.objects.create(learner=learner, course=course)
            context = {'course': course,
                       'course_id': course_id,
                       'lesson': lesson,
                       'lessons': lessons,
                       'quiz': quiz,
                       'is_done': is_done,
                       }
            return render(request, 'courses/lessonview.html', context)
        except Course.DoesNotExist:
            raise Http404("No lesson matches the given id.")

    def post(self, request, *args, **kwargs):
        done_lessons = []
        is_done = False
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        lesson_id = kwargs.get('pkl')
        print(request.POST['option'])
        try:
            user_id = request.user.id - 5
            learner = User.objects.get(id=request.user.id - 5)
            course = Course.objects.get(pk=course_id)
            lesson = Lesson.objects.get(pk=lesson_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            num_of_lessons = len(lessons)

            for i in range(len(lessons)):
                if LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=user_id).exists():
                    done_lessons.append(LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=request.user.id-5))
                    print(done_lessons)
            num_of_done_lessons = len(done_lessons)
            percent_of_done_lessons = (num_of_done_lessons / num_of_lessons * 100).__round__(1)
            if percent_of_done_lessons == 100.0 and not CoursesLearnerRelations.objects.filter(course_id=course_id, learner_id=user_id).exists():
                rel = CoursesLearnerRelations.objects.create(learner=learner, course=course)
            quiz = QuestModel.objects.get(pk=lesson.questions_id)
            if request.POST['option'].lower() == quiz.answer.lower():
                percentage = 1
            else:
                percentage = 0
            is_done = LessonsLearnerRelations.objects.create(learner=learner, lesson=lesson, percentage=percentage)
            is_done = True
            context = {'course': course,
                       'course_id': course_id,
                       'lesson': lesson,
                       'lessons': lessons,
                       'quiz': quiz,
                       'is_done': is_done,
                       'percent_of_done_lessons': percent_of_done_lessons,
                       }
            return render(request, 'courses/lessonview.html', context)
        except Course.DoesNotExist:
            raise Http404("No lesson matches the given id.")

class ProfileView(View):

    # Handles get request
    def get(self, request):
        context = {}
        # We get URL parameter pk from keyword argument list as course_id
        user_id = request.user.id - 5
        enrollments = Enrollment.objects.filter(learner_id=user_id)
        courses = []
        lessons = []
        done_lessons = []
        for enrollment in enrollments:
            lessons.append(Lesson.objects.filter(course_id=enrollment.course_id))
            courses.append(enrollment.course)

        done_lessons = LessonsLearnerRelations.objects.filter(learner_id=user_id)
        numLessons = 0
        for i in range(len(lessons)):
            numLessons += len(lessons[i])
        numDoneLessons = len(done_lessons)
        doneLessons = int(numDoneLessons / numLessons * 100)
        notDoneLessons = int(100 - doneLessons)
        show_list = ['Done', 'Not done']
        progress_list = [doneLessons, notDoneLessons]
        try:
            users = User.objects.get(pk=user_id)
            context = {'users': users,
                       'numOfEnrollments': len(enrollments),
                       'course_list': courses,
                       'show_list': show_list,
                       'progress_list': progress_list,
                       }
            return render(request, 'courses/profile.html', context)
        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")
