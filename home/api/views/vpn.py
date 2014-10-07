# -*- coding: utf-8 -*-
from django.views.generic import View

from ...utilities.vpn import Air

__author__ = 'Jon Nappi'


class VPNView(View):
    _vpn = Air()
