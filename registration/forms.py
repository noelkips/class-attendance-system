from django import forms
from .models import Registration, Attendance
from django.forms import ModelForm
from django.http import HttpResponse


class UnitRegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'


class Attendance(ModelForm):
    class Meta:
        model = Attendance
        fields = 'lecture'


"""
from django import forms
from .models import Lesson, Comment, Reply


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_id', 'name', 'position', 'video', 'ppt', 'notes')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    labels = {"body": "Comment"}

    widgets = {
        'body': forms.Textarea(attrs={
            'class': 'form-control', 'rows': 4, 'cols': 70, 'placeholder': "Enter Your Comment"
        })
    }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)

    widgets = {
        'reply_body': forms.Textarea(attrs={
            'class': 'form-control', 'rows': 2, 'cols': 10
        })
    }



"""
