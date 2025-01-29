"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia.objects.objects import DefaultCharacter
from features.room_ambience import AmbienceChararacterMixin
from features.character_magic import MagicCharacterMixin
from features.character_health import HealthCharacterMixin
from features.character_money import MoneyCharacterMixin
from features.character_clothing import ClothingCharacterMixin
from features.character_stats import StatCharacterMixin
from features.character_roleplay import ContribRPCharacter
from features.npc_talking import ConversationMixin

class Character(
                HealthCharacterMixin,
                MagicCharacterMixin,
                AmbienceChararacterMixin,
                MoneyCharacterMixin,
                ClothingCharacterMixin,
                StatCharacterMixin,
                ContribRPCharacter,
                DefaultCharacter):
    pass

class NPC(ConversationMixin, Character):
    pass