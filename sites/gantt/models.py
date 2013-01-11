# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import time
import markdown

from django.db import models
from django.utils import simplejson
from django.contrib.auth.models import User

def _fmt_date(d):
    if d:
        return "/Date(%s)/" % (time.mktime(d.timetuple()) * 1000 - 24 * 3600 * 1000)
    return ""

def _md(md, no_p=False):
    return markdown.markdown(md, ['nl2br', 'fenced_code'], safe_mode='escape') if md else ""

class Gantt(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User)
    descn = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('gantt_detail', [str(self.id)])

    def get_descn(self):
        return _md(self.descn)

    def tojson(self):
        root = []
        for prj in self.project_set.all():
            for i, task in enumerate(prj.task_set.all()):
                prj_name = prj.name if i==0 else ""
                subtasks_ = []
                task_ = {'name': prj_name, 'desc': task.name, 'values': subtasks_}
                root.append(task_)
                for subtask in task.subtask_set.all():
                    desc = _md(subtask.descn)
                    subtask_ = {'from': _fmt_date(subtask.from_date),
                            'to': _fmt_date(subtask.to_date),
                            'label': subtask.label,
                            'desc': desc,
                            'dataObj': desc,
                            'customClass': subtask.color,
                            }
                    subtasks_.append(subtask_)
        return simplejson.dumps(root)

class Project(models.Model):
    gantt = models.ForeignKey(Gantt)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return "%s - %s" % (self.gantt.name, self.name)

class Task(models.Model):
    prj = models.ForeignKey(Project)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return "%s - %s" % (self.prj, self.name)

class SubTask(models.Model):
    COLOR_CHOICES = (("ganttCoffe", "Coffe"),
            ("ganttGreen", "Green"),
            ("ganttOrange", "Orange"),
            ("ganttBlue", "Blue"),
            ("ganttRed", "Red"),
            )
    task = models.ForeignKey(Task)
    from_date = models.DateField()
    to_date = models.DateField()
    label = models.CharField(max_length=64, help_text="task owner")
    descn = models.TextField(blank=True)
    color = models.CharField(max_length=32, choices=COLOR_CHOICES)

    def __unicode__(self):
        return "%s - %s" % (self.task, self.label)
