"""
Clothing handler
The `ClothinHandler` provides an interface to manipulate a lits on the 
Character, containing the clothing worn by the Character.

ATTRIBUTES:
    obj.db.clothing (list): List of objects worn by the Character.
                         Example: [Obj, Obj, Obj ...]

INSTALLATION:
1. Have Character typeclass inherit from ClothingCharacterMixin()
    from features.character_clothing import ClothingCharacterMixin
    class Character(ClothingCharacterMixin, DefaultCharacter):
        pass

USE:
    >self.clothing.list
    [<item>, <item>]
    
TODO:
-Commands
"""

from evennia.utils import lazy_property, utils, dbserialize

# CLOTHING CHARACTER MIXIN ----------------------------------------------------

class ClothingCharacterMixin():
    """
    This is a mixin that provides Clothing functionality for Characters.

    """

    @lazy_property
    def clothing(self):
        """Handler for Character clothing."""
        return ClothingHandler(self)

    def at_object_creation(self):
        """
        Called only once, when object is first created
        """
        super().at_object_creation()

        # Values for the ClothingHandler
        self.db.clothing = [] # [Obj, Obj, Obj ...]

# CLOTHING HANDLER ------------------------------------------------------------

class ClothingException(Exception):
    """
    Base exception class for ClothingHandler.

        Args:
            msg (str): informative error message
    """
    def __init__(self, msg):
        self.msg = msg


class ClothingHandler(object):
    """Handler for a Character's Clothing.

    Args:
        obj (Character): The Parent Character object.

    Properties
        clothing (list): List of objects worn by the Character.
        
    """

    def __init__(self, obj):
        """
        Save reference to the parent typeclass and check appropriate attributes

        Args:
            obj (typeclass): Character typeclass.
        """
        self.obj = obj

        if not self.obj.attributes.has("magic"):
            msg = '`ClothingHandler` requires `db.clothing` attribute on `{}`.'
            raise ClothingException(msg.format(obj))

    @property
    def list(self):
        """
        Returns list of items worn by Character.

        Returns:
            clothing (list): List of items worn by the Character.

        Returned if:
            obj.clothing.list
        """
        return self.obj.db.clothing

    def __len__(self):
        """
        Returns number of items worn by Character.

        Returns:
            length (int): Number of items worn by Character.

        Returned if:
            len(obj.clothing)
        """
        return len(self.obj.db.clothing)

    def __bool__(self):
        """
        Support Boolean comparison for items worn by Character.

        Returns:
            Boolean: True if items worn, False if no items worn.

        Returned if:
            if obj.clothing
        """
        return bool(self.obj.db.clothing)
        
    def add(self, item, position = None, quiet=False):
        """
        Add item to Clothing list.

        Returned if:
            obj.clothing.add(item, 3)
        """
        clothing = self.obj.db.clothing

        if item in clothing:
            clothing.remove(item)

        # Add item to Clothing list
        if position is None:
            clothing.append(item)
        else:
            clothing.insert(position, item)
        
        # Telegraph
        if not quiet:
            self.obj.msg("You put on {}.".format(item.get_display_name()))
            self.obj.location.msg_contents("{} put on {}".format(self.obj.get_display_name(), item.get_display_name()))

    def remove(self, item, quiet=False):
        """
        Remove item from Clothing list.

        Returned if:
            obj.clothing.remove(item)
        """
        clothing = self.obj.db.clothing

        if item in clothing:
            clothing.remove(item)

        # Telegraph
        if not quiet:
            self.obj.msg("You take off {}.".format(item.get_display_name()))
            self.obj.location.msg_contents("{} take off {}".format(self.obj.get_display_name(), item.get_display_name()))
