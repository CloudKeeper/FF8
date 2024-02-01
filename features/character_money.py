"""
Money handler
The `MoneyHandler` provides an interface to manipulate an integer on the 
Character, representing the current Money of the Character.

ATTRIBUTES:
    obj.db.money (int): Current money of the Character.

INSTALLATION:
1. Have Character typeclass inherit from MoneyCharacterMixin()
    from features.character_health import MoneyCharacterMixin
    class Character(MoneyCharacterMixin, DefaultCharacter):
        pass

USE:
    >self.money
    100
    
TODO - FAIL IF NOT ENOUGH MONEY
"""

from evennia.utils import lazy_property

class MoneyCharacterMixin():
    """
    This is a mixin that provides Money functionality for Characters.

    """

    @lazy_property
    def Money(self):
        """Handler for Character health."""
        return MoneyHandler(self)

    def at_object_creation(self):
        """
        Called only once, when object is first created
        """
        super().at_object_creation()

        # Values for the MagicHandler
        self.db.money = 0


class MoneyException(Exception):
    """
    Base exception class for MoneyHandler.

        Args:
            msg (str): informative error message
    """
    def __init__(self, msg):
        self.msg = msg


class MoneyHandler(object):
    """Handler for a Character's Money.

    Args:
        obj (Character): The Parent Character object.

    Properties
        money (int): Current money of Character.

    """

    def __init__(self, obj):
        """
        Save reference to the parent typeclass and check appropriate attributes

        Args:
            obj (typeclass): Character typeclass.
        """
        self.obj = obj

        if not self.obj.attributes.has("health"):
            msg = 'MoneyHandler` requires `db.money` attribute on `{}`.'
            raise MoneyException(msg.format(obj))
   
   # Current Money
   
    def __repr__(self):
        """
        Current money as string

        Returns:
            Money (str): Current money of Character.

        Returned if:
            str(obj.money)
        """
        return str(self.obj.db.money)
    
    def __bool__(self):
        """
        Support Boolean comparison for money of the Character.

        Returns:
            Boolean: True if money > 0.

        Returned if:
            if obj.money
        """
        return bool(self.obj.db.money)

    @property
    def current(self):
        """
        Current money as integer
        
        Returns:
            Money (int): Character's current money.
            
        Returned if:
            obj.money.current
        """
        return int(self.obj.db.money)

    # Money Arithmatic
        
    def __add__(self, value):
        """
        Support addition operator for Character money.
        
        Returns:
            Money (int): Money after addition.
            
        Returned if:
            obj.money + 5
        """
        
        self.obj.db.money += int(value)
        if self.obj.db.money <= 0:
            self.obj.db.money = 0
            return
        return self.obj.db.money
    
    def add(self, value=0):
        """
        Add value to Character money.
        
        Returns:
            Money (int): Money after addition.
            
        Returned if:
            obj.money.add(5)
        """
        
        return self.__add__(value)

    def __sub__(self, value):
        """
        Support subtraction operator for Character money.
        
        Returns:
            Money (int): Money after subtraction.
            
        Returned if:
            obj.money - 5
        """
        self.obj.db.money -= int(value)
        if self.obj.db.money <= 0:
            self.obj.db.money = 0
            return
        return self.obj.db.money

    def sub(self, value=0):
        """
        Subtract value from Character money.
        
        Returns:
            Health (int): Health after subtraction.
            
        Returned if:
            obj.money.sub(5)
        """
        
        return self.__sub__(value)

    def __mul__(self, value):
        """
        Multiply value with Character money.
        
        Returns:
            Money (int): Money after multiplication.
            
        Returned if:
            obj.money * 5
        """
        self.obj.db.money * int(value)
        if self.obj.db.money <= 0:
            self.obj.db.money = 0
            return
        return self.obj.db.money

    def __truediv__(self, value):
        """
        Divide Character money with value.
        
        Returns:
            Money (int): Money after division.
            
        Returned if:
            obj.money / 5
        """
        self.obj.db.money / int(value)
        if self.obj.db.money <= 0:
            self.obj.db.money = 0
            return
        return self.obj.db.money

    # Money Comparisons

    def __eq__(self, value):
        """
        Support equality comparison between money and int.
        
        Returns:
            Boolean: True if equal, False if not.
            
        Returned if:
            obj.money == 5
        """
        return self.obj.db.money == int(value)

    def __ne__(self, value):
        """
        Support non-equality comparison between money and int.
        
        Returns:
            Boolean: True if not equal, False if equal.
            
        Returned if:
            obj.money != 5
        """
        return self.obj.db.money != int(value)

    def __lt__(self, value):
        """
        Support less than comparison between money and int.
        
        Returns:
            Boolean: True if less than, False if not.
            
        Returned if:
            obj.money < 5
        """
        return self.obj.db.money < int(value)

    def __le__(self, value):
        """
        Support less than or equal to comparison between money and int.
        
        Returns:
            Boolean: True if less than or equal, False if not.
            
        Returned if:
            obj.money <= 5
        """
        return self.obj.db.money <= int(value)

    def __gt__(self, value):
        """
        Support greater than comparison between money and int.
        
        Returns:
            Boolean: True if greater than, False if not.
            
        Returned if:
            obj.money > 5
        """
        return self.obj.db.money > int(value)

    def __ge__(self, value):
        """
        Support greater than or equal to comparison between money and int.
        Returns:
            Boolean: True if greater than or equal, False if not.
            obj.money >= 5
        """
        return self.obj.db.money >= int(value)
            