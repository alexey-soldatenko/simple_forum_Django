from django.db import models

# Create your models here.
class Sections(models.Model):
	section_name = models.CharField(max_length=30)
	def __str__(self):
		return self.section_name

class Subsection(models.Model):
	section_name = models.ForeignKey(Sections, default='other')
	subsection_name = models.CharField(max_length=50)
	def __str__(self):
		return self.subsection_name

class Topics(models.Model):
	section_name = models.ForeignKey(Sections, default='other')
	subsection_name = models.ForeignKey(Subsection, default='other')
	topic_name = models.CharField(max_length=300)
	date = models.DateField()
	author_name = models.CharField(max_length=100)
	context = models.TextField()

	def __str__(self):
		return self.topic_name

class TopicAnswers(models.Model):
	topic_name = models.ForeignKey(Topics)
	user_name = models.CharField(max_length=100)
	date = models.DateField()
	context = models.TextField()

