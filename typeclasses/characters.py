"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia.objects.objects import DefaultCharacter
from features.room_ambience import AmbientChararacterMixin
from features.character_magic import MagicCharacterMixin

class Character(MagicCharacterMixin, AmbientChararacterMixin, DefaultCharacter):

    pass
