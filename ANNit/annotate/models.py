from django.db import models



class Choice(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, default = 'TBD')
    # votes = models.IntegerField(default=0)
    # votes = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text


class Entry(models.Model):
    URI_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')
    user_choice = models.CharField(max_length=200, default = 'TBD')
    comment = models.CharField(max_length=400, default = 'TBD')

    def __str__(self):
        return self.URI_text
    def needs_anno(self):
        return self.user_choice == 'TBD'
