from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Division(models.Model):
	user = models.ForeignKey(User, null=True)
	name = models.CharField(max_length = 42, unique=True)

	def __unicode__(self):
		return self.name


class Board(models.Model):
	division = models.ForeignKey(Division)
	user = models.ForeignKey(User, null=True)
	name = models.CharField(max_length=666)

	def __unicode__(self):
		return self.name


class Comment(models.Model):
	user = models.ForeignKey(User, null=True)
	board = models.ForeignKey(Board)
	text = models.TextField(default="")

	def __unicode__(self):
		return self.text