from django.db import models



class Choice(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)
    # votes = models.BooleanField(default=False)


class Entry(models.Model):
    URI_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')
    user_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
