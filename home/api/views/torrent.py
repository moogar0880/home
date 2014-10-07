# -*- coding: utf-8 -*-
from django.views.generic import View

from ...utilities.torrent import Transmission

__author__ = 'Jon Nappi'


class TorrentView(View):
    _client = Transmission()

    def get(self):
        pass

    def post(self):
        pass
