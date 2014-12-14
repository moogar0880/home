# -*- coding: utf-8 -*-
import plistlib
from collections import namedtuple, OrderedDict

__author__ = 'Jon Nappi'


"""
from itunes import Library
l = Library()

"""


class Library:
    """iTunes Library interface utility class"""
    library_path = '/Users/Jon/Desktop/iTunes Music Library.xml'

    def __init__(self):
        self.tracks = self.date = self.playlists = self.minor_version = None
        self.major_version = self.library_persistent_id = self.features = None
        self.show_content_ratings = self.application_version = None
        self.music_folder = None

        class attribdict(OrderedDict):
            """Force dict keys to be sutable class attribute names"""
            def __setitem__(self, key, value, **kwargs):
                super().__setitem__(key.lower().replace(' ', '_'), value,
                                    **kwargs)

        with open(self.library_path, 'rb') as f:
            library_data = plistlib.load(f, dict_type=attribdict)

        for key, val in library_data.items():
            if key == 'tracks':
                self.tracks = []
                Track = lambda self: object()
                for i_key in val.keys():
                    Track = namedtuple('Track', [k for k in val[i_key].keys()])
                    break
                # import pdb; pdb.set_trace()
                for track_id, track_data in val.items():
                    self.tracks.append(Track(*[i for i in track_data]))
            else:
                setattr(self, key, val)

    @property
    def tv_shows(self):
        """A list of TV Shows contained in this iTunes library"""
        return [track for track in self.tracks if track.tv_show]
