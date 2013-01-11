# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from .models import Gantt

def index(request):
    template_name = 'gantt/index.html'
    return render(request, template_name, 
            {'gantts': Gantt.objects.all()})

def detail(request, pk):
    template_name = 'gantt/detail.html'
    gantt = get_object_or_404(Gantt, pk=pk)
    return render(request, template_name, 
            {'gantt': gantt,
                'gantt_json': gantt.tojson()})
