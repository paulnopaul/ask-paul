from django import forms
from app.models import Question, Profile, Answer
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    def save(self, *args, **kwargs):
        user = kwargs.pop('user')
        question = super().save(*args, **kwargs)
        question.user = user
        question.save()
        return question


class UserSignupForm(forms.ModelForm):
    avatar = forms.ImageField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save(self, *args, **kwargs):
        user = kwargs.pop('user')
        answer = super().save(*args, **kwargs)
        answer.user = user
        answer.save()
