from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='questions')
    likes = models.ManyToManyField(to=User, related_name='question_likes')
    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.OneToOneField(to=Question, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='answers')

