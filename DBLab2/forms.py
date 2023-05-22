from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Enrollment


class NewLearnerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    social_link = forms.URLField(max_length=200)
    is_instructor = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "social_link", "is_instructor")

    def save(self, commit=True):
        learner = super(NewLearnerForm, self).save(commit=False)
        learner.email = self.cleaned_data['email']
        learner.is_instructor = self.cleaned_data['is_instructor']
        learner.social_link = self.cleaned_data['social_link']
        if commit:
            learner.save()
            print(learner)
        return learner

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'distributor_name', 'pub_date']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['user', 'course', 'date_enrolled', 'progress']
