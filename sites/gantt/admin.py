# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib import admin

from .models import Gantt, Project, Task, SubTask

class ProjectInline(admin.TabularInline):
    model = Project

class GanttAdmin(admin.ModelAdmin):
    search_fields       = ('name',)
    inlines = [
        ProjectInline,
    ]

class TaskInline(admin.TabularInline):
    model = Task

class ProjectAdmin(admin.ModelAdmin):
    search_fields       = ("gantt__name", 'name')
    inlines = [
        TaskInline,
    ]

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    search_fields       = ("prj__gantt__name", "prj__name", 'name')
    inlines = [
        SubTaskInline,
    ]

class SubTaskAdmin(admin.ModelAdmin):
    search_fields       = ("task__prj__gantt__name", "task__prj__name", "task__name", 'name')

admin.site.register(Gantt, GanttAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
