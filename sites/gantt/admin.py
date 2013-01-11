# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib import admin

from .models import Gantt, Project, Task, SubTask

class ProjectInline(admin.TabularInline):
    model = Project

def owner__name(obj):
    return "%s" % obj.owner

class GanttAdmin(admin.ModelAdmin):
    search_fields       = ('name',)
    list_display = ('__unicode__', owner__name)
    exclude = ('owner',)
    inlines = [
        ProjectInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def queryset(self, request):
        qs = super(GanttAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

class TaskInline(admin.TabularInline):
    model = Task

class ProjectAdmin(admin.ModelAdmin):
    search_fields       = ("gantt__name", 'name')
    list_filter         = ('gantt',)
    raw_id_fields       = ("gantt",)
    inlines = ( TaskInline, )

    def queryset(self, request):
        qs = super(ProjectAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(gantt__owner=request.user)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    search_fields       = ("prj__gantt__name", "prj__name", 'name')
    list_filter         = ('prj',)
    raw_id_fields       = ("prj",)
    inlines = [
        SubTaskInline,
    ]

    def queryset(self, request):
        qs = super(TaskAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(prj__gantt__owner=request.user)

class SubTaskAdmin(admin.ModelAdmin):
    search_fields       = ("task__prj__gantt__name", "task__prj__name", "task__name", 'name')
    list_filter         = ('task',)
    raw_id_fields       = ("task",)

    def queryset(self, request):
        qs = super(SubTaskAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(task__prj__gantt__owner=request.user)

admin.site.register(Gantt, GanttAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
