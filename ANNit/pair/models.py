from django.db import models

# Create your models here.

class Choice(models.Model):
	equal =  'equal'
	left_more_general = 'left>right'
	right_more_general = 'left<right'
	neither = 'neither'
	unknown = 'unknown'

	# question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200, default = 'TBD')
	# votes = models.IntegerField(default=0)
	# votes = models.BooleanField(default=False)
	def __str__(self):
		return self.choice_text


class Entry(models.Model):
	left_URI_text = models.CharField(max_length=200, default="left")
	right_URI_text = models.CharField(max_length=200, default="right")
	# pub_date = models.DateTimeField('date published')
	user_choice = models.CharField(max_length=200, default = 'TBD')
	user_decision = models.CharField(max_length=200, default = 'TBD')
	comment = models.CharField(max_length=400, default = 'TBD')

	def __str__(self):
		return self.left_URI_text + self.right_URI_text
	def needs_anno(self):
		return self.user_choice == 'TBD'
