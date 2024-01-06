"""
Health handler
The `HealthHandler` provides an interface to manipulate an integer on the 
Character, representing the current health of the Character.

ATTRIBUTES:
    obj.db.health (int): Current health of the Character.

INSTALLATION:
1. Have Character typeclass inherit from HealthCharacterMixin()
    from features.character_health import HealthCharacterMixin
    class Character(HealthCharacterMixin, DefaultCharacter):
        pass

USE:
    self.health
    100
"""

from evennia.utils import lazy_property

class HealthCharacterMixin():
    """
    This is a mixin that provides Health functionality for Characters.

    """

    @lazy_property
    def Health(self):
        """Handler for Character health."""
        return HealthHandler(self)

    def at_object_creation(self):
        """
        Called only once, when object is first created
        """
        super().at_object_creation()

        # Values for the MagicHandler
        self.db.health = 1


class HealthException(Exception):
    """
    Base exception class for HealthHandler.

        Args:
            msg (str): informative error message
    """
    def __init__(self, msg):
        self.msg = msg


class HealthHandler(object):
    """Handler for a Character's Health.

    Args:
        obj (Character): The Parent Character object.

    Properties
        health (int): Current health of Character.

    Methods:
        ...
    """

    def __init__(self, obj):
        """
        Save reference to the parent typeclass and check appropriate attributes

        Args:
            obj (typeclass): Character typeclass.
        """
        self.obj = obj

        if not self.obj.attributes.has("health"):
            msg = '`HealthHandler` requires `db.health` attribute on `{}`.'
            raise HealthException(msg.format(obj))

    # Character alive or dead
    
    def __bool__(self):
        """
        Support Boolean comparison for health of the Character.

        Returns:
            Boolean: True if health > 0.

        Returned if:
            if obj.health
        """
        return bool(self.obj.db.health)

    def alive(self):
        """
        Returns Boolean for health of the Character.

        Returns:
            Boolean: True if health > 0.

        Returned if:
            if obj.health.alive()
        """
        return bool(self.obj.db.health)
    
    def death(self):
        """
        Implement Character death response.

        """
        # TODO - Death code.
        return

    # Full Health

    @property
    def max(self):
        """
        Calculate maximum health of the Character.

        Returns:
            Max health (int) - Max health of Character.

        Returned if:
            if obj.health.max
        """
        # TO DO - Max Health Calculation
        return 100

    def reset(self):
        """
        Returns Character health to maximum.

        Returns:
            Current health (int) - Health after reset.

        Returned if:
            obj.health.reset
        """
        
        self.obj.db.health = self.max
        
        return self.obj.db.health

    # Current Health

    @property
    def current(self):
        """
        Current health as integer
        
        Returns:
            Health (int): Character's current health.
            
        Returned if:
            obj.health.current
        """
        return int(self.obj.db.health)

    def __repr__(self):
        """
        Current health as string

        Returns:
            Health (str): Current health of Character.

        Returned if:
            str(obj.health)
        """
        return str(self.obj.db.health)

    @property
    def percentage(self):
        """
        Current health as percentage.
        
        Returns:
            Health (int): Characters current health as percentage of max.
            
        Returned if:
            obj.heatlh.percent
        """
        return (self.current * 100.0 / self.max)

    # Health Arithmatic
        
    def __add__(self, value):
        """
        Support addition operator for Character health.
        
        Returns:
            Health (int): Health after addition.
            
        Returned if:
            obj.health + 5
        """
        
        self.obj.db.health += int(value)
        
        if self.obj.db.health > self.max:
            self.obj.db.health = self.max
        if self.obj.db.health <= 0:
            self.death()
            return
        
        return self.obj.db.health
    
    def add(self, value=0):
        """
        Add value to Character health.
        
        Returns:
            Health (int): Health after addition.
            
        Returned if:
            obj.health.add(5)
        """
        
        return self.__add__(value)

    def __sub__(self, value):
        """
        Support subtraction operator for Character health.
        
        Returns:
            Health (int): Health after subtraction.
            
        Returned if:
            obj.heatlh - 5
        """
        self.obj.db.health -= int(value)
        
        if self.obj.db.health > self.max:
            self.obj.db.health = self.max
        if self.obj.db.health <= 0:
            self.death()
            return
        
        return self.obj.db.health

    def sub(self, value=0):
        """
        Subtract value from Character health.
        
        Returns:
            Health (int): Health after subtraction.
            
        Returned if:
            obj.health.sub(5)
        """
        
        return self.__sub__(value)

    def __mul__(self, value):
        """
        Multiply value with Character health.
        
        Returns:
            Health (int): Health after multiplication.
            
        Returned if:
            obj.heatlh * 5
        """
        self.obj.db.health * int(value)
        
        if self.obj.db.health > self.max:
            self.obj.db.health = self.max
        if self.obj.db.health <= 0:
            self.death()
            return
        
        return self.obj.db.health

    def __truediv__(self, value):
        """
        Devide Character health with value.
        
        Returns:
            Health (int): Health after devision.
            
        Returned if:
            obj.heatlh / 5
        """
        self.obj.db.health / int(value)
        
        if self.obj.db.health > self.max:
            self.obj.db.health = self.max
        if self.obj.db.health <= 0:
            self.death()
            return
        
        return self.obj.db.health

    # Health Comparisons

    def __eq__(self, value):
        """
        Support equality comparison between health and int.
        
        Returns:
            Boolean: True if equal, False if not.
            
        Returned if:
            obj.heatlh == 5
        """
        return self.obj.db.health == int(value)

    def __ne__(self, value):
        """
        Support non-equality comparison between health and int.
        
        Returns:
            Boolean: True if not equal, False if equal.
            
        Returned if:
            obj.heatlh != 5
        """
        return self.obj.db.health != int(value)

    def __lt__(self, value):
        """
        Support less than comparison between health and int.
        
        Returns:
            Boolean: True if less than, False if not.
            
        Returned if:
            obj.heatlh < 5
        """
        return self.obj.db.health < int(value)

    def __le__(self, value):
        """
        Support less than or equal to comparison between health and int.
        
        Returns:
            Boolean: True if less than or equal, False if not.
            
        Returned if:
            obj.heatlh <= 5
        """
        return self.obj.db.health <= int(value)

    def __gt__(self, value):
        """
        Support greater than comparison between health and int.
        
        Returns:
            Boolean: True if greater than, False if not.
            
        Returned if:
            obj.heatlh > 5
        """
        return self.obj.db.health > int(value)

    def __ge__(self, value):
        """
        Support greater than or equal to comparison between health and int.
        Returns:
            Boolean: True if greater than or equal, False if not.
        Returned if:
            obj.heatlh >= 5
        """
        return self.obj.db.health >= int(value)
            