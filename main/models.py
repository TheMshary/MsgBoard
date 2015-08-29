from django.db import models
from django.contrib.auth.models import User
from itertools import chain

# Create your models here.


class Division(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=42, unique=True)

    def __unicode__(self):
        return self.name


class Board(models.Model):
    division = models.ForeignKey("main.Division")
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=666)

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, null=True)
    board = models.ForeignKey("main.Board")
    text = models.TextField(default="")
    parent_comment = models.ForeignKey("main.Comment", null=True, default=None)

    def __unicode__(self):
        return self.text
