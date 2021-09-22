from django.conf import settings
from django.db import models
from django.utils import timezone


class Survey(models.Model):
    
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField(help_text='For example: 2021-08-24 16:43:52')
    finish_date = models.DateTimeField(blank=True,
                                       null=True,
                                       help_text='For example: 2021-08-28 00:43:35')
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):

    ANSWER_TYPE_CHOICES = [
        ('ta', 'Text answer'),
        ('uv', 'Unique variant choice'),
        ('sv', 'Choice set of variants'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    answer_type = models.CharField(
        max_length=2,
        choices=ANSWER_TYPE_CHOICES,
        default='ta')

    def __str__(self):
        return self.text


class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.text


class Customer(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.pk)


class CompletedSurvey(models.Model):

    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class GivenAnswer(models.Model):

    completed_survey = models.ForeignKey(CompletedSurvey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.TextField() # Declarate a necessary copying for a text of an answer

    def __str__(self):
        return self.answer
