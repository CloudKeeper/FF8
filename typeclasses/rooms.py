"""
Room

Rooms are simple container objects that have no location of their own.

"""

from evennia import DefaultRoom
from features.room_details import DetailRoomMixin
from features.room_ambience import AmbientRoomMixin

class Room(AmbientRoomMixin, DetailRoomMixin, DefaultRoom):

    pass
