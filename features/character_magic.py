"""
Magic handler
The `MagicHandler` provides an interface to manipulate a dictionary on the 
Character, containing the magic the Character possesses.

ATTRIBUTES:
    obj.db.magic (dict): List and number of magic held by the Character.
                         Example: {"Fire" : 100, "Blizzard" : 100}

INSTALLATION:
1. Have Room typeclass inherit from MagicCharacterMixin()
    from features.character_magic import MagicCharacterMixin
    class Character(MagicCharacterMixin, DefaultCharacter):
        pass

USE:
    self.magic.list
    [<magic>, <magic>]
"""

from evennia.utils import lazy_property, utils, dbserialize

# MAGIC LIST -----------------------------------------------------------------
# To replace with a database or flatfile dedicated to these values.

magic_list = {
    "Fire" : "Fire",
    "Fira" : "Fira",
    "Firaga" : "Firaga",
    "Blizzard" : "Blizzard",
    "Blizzara" : "Blizzara",
    "Blizzaga" : "Blizzaga",
    "Thunder" : "Thunder",
    "Thundara" : "Thundara",
    "Thundaga" : "Thundaga",
    "Water" : "Water",
    "Aero" : "Aero",
    "Bio" : "Bio",
    "Demi" : "Demi",
    "Quake" : "Quake",
    "Tornado" : "Tornado",
    "Holy" : "Holy",
    "Flare" : "Flare",
    "Meteor" : "Meteor",
    "Ultima" : "Ultima",
    "Cure" : "Cure",
    "Cura" : "Cura",
    "Curaga" : "Curaga",
    "Life" : "Life",
    "Full-life" : "Full-life",
    "Regen" : "Regen",
    "Esuna" : "Esuna",
    "Scan" : "Scan",
    "Sleep" : "Sleep",
    "Blind" : "Blind",
    "Silence" : "Silence",
    "Confuse" : "Confuse",
    "Berserk" : "Berserk",
    "Break" : "Break",
    "Zombie" : "Zombie",
    "Death" : "Death",
    "Double" : "Double",
    "Triple" : "Triple",
    "Dispel" : "Dispel",
    "Protect" : "Protect",
    "Shell" : "Shell",
    "Reflect" : "Reflect",
    "Float" : "Float",
    "Drain" : "Drain",
    "Haste" : "Haste",
    "Slow" : "Slow",
    "Stop" : "Stop",
    "Meltdown" : "Meltdown",
    "Pain" : "Pain",
    "Aura" : "Aura",
    "Apocalypse" : "Apocalypse"
}

# MAGIC CHARACTER MIXIN ------------------------------------------------------

class MagicCharacterMixin():
    """
    This is a mixin that provides Magic functionality for Characters.

    """

    @lazy_property
    def magic(self):
        """Handler for Character magic."""
        return MagicHandler(self)

    def at_object_creation(self):
        """
        Called only once, when object is first created
        """
        super().at_object_creation()

        # Values for the MagicHandler
        self.db.magic = {} # {"Fire" : 100, "Blizzard" : 100}

# MAGIC HANDLER --------------------------------------------------------------

class MagicException(Exception):
    """
    Base exception class for MagicHandler.

        Args:
            msg (str): informative error message
    """
    def __init__(self, msg):
        self.msg = msg


class MagicHandler(object):
    """Handler for a Character's Magic.

    Args:
        obj (Character): The Parent Character object.

    Properties
        magic (dict): List and number of magic held by the Character.

    Methods:
        list (list): Returns list of Magic possessed by the Character.
        add (str): add x magic to given spell, or creates spell if didn't exist.
        remove (str): remove x magic from given spell, or spell itself if at 0.
        amount (int): Return amount of Magic left for given spell.
    """

    def __init__(self, obj):
        """
        Save reference to the parent typeclass and check appropriate attributes

        Args:
            obj (typeclass): Pokemon typeclass.
        """
        self.obj = obj

        if not self.obj.attributes.has("magic"):
            msg = '`MagicHandler` requires `db.magic` attribute on `{}`.'
            raise MagicException(msg.format(obj))

    @property
    def list(self):
        """
        Returns list of Magic possessed by the Character.

        Returns:
            magic (list): List of current Magic known to Character.

        Returned if:
            obj.magic.list
        """
        return self.obj.db.magic.keys()

    def __len__(self):
        """
        Returns number of Magic known to Character.

        Returns:
            length (int): Number of Magic known to Character.

        Returned if:
            len(obj.magic)
        """
        return len(self.obj.db.magic)

    def __nonzero__(self):
        """
        Support Boolean comparison for Magic held by Character.

        Returns:
            Boolean: True if holds Magic, False if no Magic.

        Returned if:
            if obj.magic
        """
        return bool(self.obj.db.magic)

    def amount(self, magic):
        """
        Returns the number of selected <magic> held by the Character.

        Returned if:
            obj.magic.amount("Fire")
        """
        return self.obj.db.magic.get(magic, 0)
        
    def add(self, magic, number = 1):
        """
        Increase selected <magic> by <number> respecting limit of 100.

        Returned if:
            obj.magic.add("Fire", 10)
        """
        if not magic in magic_list:
            msg = "Arguments passed to `MagicHandler.add()` caused an error."
            raise MagicException(msg)
        
        try:
            self.obj.db.magic[magic] = self.obj.db.magic.get(magic, 0) + int(number)
        except:
            msg = "Arguments passed to `MagicHandler.add()` caused an error."
            raise MagicException(msg)
        
        if self.obj.db.magic[magic] > 100:
            self.obj.db.magic[magic] = 100
        if self.obj.db.magic[magic] < 1:
            del self.obj.db.magic[magic]
        return True

    def remove(self, magic, number = 1):
        """
        Reduce selected <magic> by <number>, removing <magic> if 0.

        Returned if:
            obj.magic.remove("Fire", 10)
        """
        if not magic in magic_list:
            msg = "Arguments passed to `MagicHandler.remove()` caused an error."
            raise MagicException(msg)
        
        try:
            self.obj.db.magic[magic] = self.obj.db.magic[magic] - int(number)
        except:
            msg = "Arguments passed to `MagicHandler.remove()` caused an error."
            raise MagicException(msg)
        
        if self.obj.db.magic[magic] > 100:
            self.obj.db.magic[magic] = 100
        if self.obj.db.magic[magic] < 1:
            del self.obj.db.magic[magic]
        return True