from django import forms
from .models import Question, Answer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        return Answer.objects.create(**self.cleaned_data)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        return User.objects.create(**self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        self._user.username = self.cleaned_data['username']
        self._user.password = self.cleaned_data['password']
        return self._user
