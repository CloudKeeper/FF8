"""
Stat handler
The `StatHandler` provides an interface to manipulate a dictionary on the 
Character, containing the stats the Character possesses.

ATTRIBUTES:
    obj.db.stats (dict): List and number of stats held by the Character.
                         Example: {"str" : 100, "def" : 100}

INSTALLATION:
1. Have Character typeclass inherit from StatCharacterMixin()
    from features.character_stats import StatCharacterMixin
    class Character(StatCharacterMixin, DefaultCharacter):
        pass

USE:
    self.stats.str
    100
"""

from evennia.utils import lazy_property, utils, dbserialize


# Stat CHARACTER MIXIN ------------------------------------------------------

class StatCharacterMixin():
    """
    This is a mixin that provides stats functionality for Characters.

    """

    @lazy_property
    def stats(self):
        """Handler for Character stats."""
        return StatHandler(self)

    def at_object_creation(self):
        """
        Called only once, when object is first created
        """
        super().at_object_creation()

        # Base Values for the StatHandler
        self.db.stats = {
            "str":8,
            "vit":8,
            "mag":8,
            "spr":8,
            "spd":8,
            "eva":0,
            "hit":100,
            "luck":0
        }

# Stat HANDLER --------------------------------------------------------------

class StatException(Exception):
    """
    Base exception class for StatHandler.

        Args:
            msg (str): informative error message
    """
    def __init__(self, msg):
        self.msg = msg


class StatHandler(object):
    """Handler for a Character's stats.

    Args:
        obj (Character): The Parent Character object.

    Properties
        stats (dict): List and number of stats held by the Character.

    """

    def __init__(self, obj):
        """
        Save reference to the parent typeclass and check appropriate attributes

        Args:
            obj (typeclass): Character typeclass.
        """
        self.obj = obj

        if not self.obj.attributes.has("stats"):
            msg = '`StatHandler` requires `db.stats` attribute on `{}`.'
            raise StatException(msg.format(obj))

    @property
    def base_str(self):
        """
        Returns base strength of the Character.

        Returns:
            strength (int): Base strength of the Character.

        Returned if:
            obj.stats.base_str
        """
        return self.obj.db.stats["str"]

    @property
    def str(self):
        """
        Calculates strength of the Character.

        Returns:
            strength (int): Current strength of the Character.

        Returned if:
            obj.stats.str
        """
        strength = self.obj.db.stats["str"]
        
        # strength stat calculation
        
        return strength

    @property
    def base_vit(self):
        """
        Returns base vitality of the Character.

        Returns:
            vitality (int): Base vitality of the Character.

        Returned if:
            obj.stats.base_vit
        """
        return self.obj.db.stats["vit"]

    @property
    def vit(self):
        """
        Calculates vitality of the Character.

        Returns:
            vitality (int): Current vitality of the Character.

        Returned if:
            obj.stats.vit
        """
        vitality = self.obj.db.stats["vit"]
        
        # vitality stat calculation
        
        return vitality

    @property
    def base_mag(self):
        """
        Returns base magic of the Character.

        Returns:
            magic (int): Base magic of the Character.

        Returned if:
            obj.stats.base_mag
        """
        return self.obj.db.stats["mag"]

    @property
    def mag(self):
        """
        Calculates magic of the Character.

        Returns:
            magic (int): Current magic of the Character.

        Returned if:
            obj.stats.mag
        """
        magic = self.obj.db.stats["mag"]
        
        # magic stat calculation
        
        return magic

    @property
    def base_spr(self):
        """
        Returns base spirit of the Character.

        Returns:
            spirit (int): Base spirit of the Character.

        Returned if:
            obj.stats.base_spr
        """
        return self.obj.db.stats["spr"]

    @property
    def spr(self):
        """
        Calculates spirit of the Character.

        Returns:
            spirit (int): Current spirit of the Character.

        Returned if:
            obj.stats.spr
        """
        spirit = self.obj.db.stats["spr"]
        
        # spirit stat calculation
        
        return spirit

    @property
    def base_spd(self):
        """
        Returns base speed of the Character.

        Returns:
            speed (int): Base speed of the Character.

        Returned if:
            obj.stats.base_spd
        """
        return self.obj.db.stats["spd"]

    @property
    def spd(self):
        """
        Calculates speed of the Character.

        Returns:
            speed (int): Current speed of the Character.

        Returned if:
            obj.stats.spd
        """
        speed = self.obj.db.stats["spd"]
        
        # speed stat calculation
        
        return speed

    @property
    def base_eva(self):
        """
        Returns base evasion of the Character.

        Returns:
            evasion (int): Base evasion of the Character.

        Returned if:
            obj.stats.base_eva
        """
        return self.obj.db.stats["eva"]

    @property
    def eva(self):
        """
        Calculates evasion of the Character.

        Returns:
            evasion (int): Current evasion of the Character.

        Returned if:
            obj.stats.eva
        """
        evasion = self.obj.db.stats["eva"]
        
        # evasion stat calculation
        
        return evasion

    @property
    def base_hit(self):
        """
        Returns base hit of the Character.

        Returns:
            hit (int): Base hit of the Character.

        Returned if:
            obj.stats.base_hit
        """
        return self.obj.db.stats["hit"]

    @property
    def hit(self):
        """
        Calculates hit of the Character.

        Returns:
            hit (int): Current hit of the Character.

        Returned if:
            obj.stats.hit
        """
        hit = self.obj.db.stats["hit"]
        
        # hit stat calculation
        
        return hit

    @property
    def base_luck(self):
        """
        Returns base luck of the Character.

        Returns:
            luck (int): Base luck of the Character.

        Returned if:
            obj.stats.base_luck
        """
        return self.obj.db.stats["luck"]

    @property
    def luck(self):
        """
        Calculates luck of the Character.

        Returns:
            luck (int): Current luck of the Character.

        Returned if:
            obj.stats.luck
        """
        luck = self.obj.db.stats["luck"]
        
        # luck stat calculation
        
        return luck

    # def add(self, magic, number = 1, quiet=False):
    #     """
    #     Increase selected <magic> by <number> respecting limit of 100.

    #     Returned if:
    #         obj.magic.add("Fire", 10)
    #     """
    #     if not magic in magic_list:
    #         msg = "Arguments passed to `MagicHandler.add()` caused an error."
    #         raise MagicException(msg)
            
    #     if not int(number) > 0:
    #         msg = "Arguments passed to `MagicHandler.add()` caused an error."
    #         raise MagicException(msg)
        
    #     current_number = self.obj.db.magic.get(magic, 0)
        
    #     if current_number == 100:
    #         self.obj.msg("You are already fully stocked with {magic}.".format(magic=magic))
    #         return False

    #     final_number = current_number + int(number)

    #     if final_number > 100:
    #         final_number = 100
    #         number = final_number - current_number
        
    #     self.obj.db.magic = final_number
        
    #     if not quiet:
    #         self.obj.msg("You stocked {number} {magic}.".format(number=number, magic=magic))
            
    #     return True

    # def remove(self, magic, number = 1):
    #     """
    #     Reduce selected <magic> by <number>, removing <magic> if 0.

    #     Returned if:
    #         obj.magic.remove("Fire", 10)
    #     """
    #     if not magic in magic_list:
    #         msg = "Arguments passed to `MagicHandler.remove()` caused an error."
    #         raise MagicException(msg)
        
    #     try:
    #         self.obj.db.magic[magic] = self.obj.db.magic[magic] - int(number)
    #     except:
    #         msg = "Arguments passed to `MagicHandler.remove()` caused an error."
    #         raise MagicException(msg)
        
    #     if self.obj.db.magic[magic] > 100:
    #         self.obj.db.magic[magic] = 100
    #     if self.obj.db.magic[magic] < 1:
    #         del self.obj.db.magic[magic]
    #     return True