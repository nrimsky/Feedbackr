from django.db import models
from django.contrib.auth.models import User

class QuestionSet(models.Model):
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class YesNoQuestion(models.Model):
    prompt = models.CharField(max_length=2000)
    completion = models.CharField(max_length=2000)
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.prompt) > 100:
            return self.prompt[:100]
        return self.prompt