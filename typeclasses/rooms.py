"""
Room

Rooms are simple container objects that have no location of their own.

"""

from evennia import DefaultRoom
from features.room_details import DetailMixin

class Room(DetailMixin, DefaultRoom):

    pass
