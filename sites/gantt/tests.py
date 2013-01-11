# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    fixtures = ['test_gantt.json']

    def test_index(self):
        resp = self.client.get(reverse('gantt_index'))
        self.assertEqual(resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(reverse('gantt_detail', args=(1,)))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('gantt_detail', args=(9999,)))
        self.assertEqual(resp.status_code, 404)
