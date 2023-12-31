"""
Object

The Object is the "naked" base class for things in the game world.

"""

from evennia.objects.objects import DefaultObject
from features.room_ambience import AmbientObjectMixin

class Object(AmbientObjectMixin, DefaultObject):

    pass
