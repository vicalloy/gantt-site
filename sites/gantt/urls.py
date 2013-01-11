# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='gantt_index'),
        url(r'^(?P<pk>\d+)/$', views.detail, name='gantt_detail'),
)
