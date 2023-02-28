from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-pk')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(
        to=User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    likes = models.ManyToManyField(to=User, related_name='question_likes')
    objects = QuestionManager()

    def get_url(self):
        return reverse('question_details', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name='answer_set')
    author = models.ForeignKey(
        to=User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    def __unicode__(self):
        return self.text
