"""
Object

The Object is the "naked" base class for things in the game world.

"""

from evennia.objects.objects import DefaultObject
from features.room_ambience import AmbienceObjectMixin
from features.character_roleplay import ContribRPObject

class Object(AmbienceObjectMixin,
             ContribRPObject,
             DefaultObject):

    pass
