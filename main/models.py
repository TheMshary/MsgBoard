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
    parent_comment = models.ForeignKey("main.Comment", null=True)

    def get_all_nested_comments(self, include_self=False):
        qs = []
        if include_self:
            qs.append(self)
        for item in Comment.objects.filter(parent_comment=self):
            # extend() puts values from second list to the end of the first
            # list
            qs.extend(item.get_all_nested_comments(include_self=True))

        # chain() takes multiple iterables and returns them as a single
        # iterable
        return chain([q for q in qs])

    def __unicode__(self):
        return self.text
