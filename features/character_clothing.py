"""
Clothing handler
The `ClothinHandler` provides an interface to manipulate a list on the 
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
-Return Appearance
"""

from evennia.utils import lazy_property, utils, dbserialize
from django.conf import settings
COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)

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
        
    def __contains__(self, item):
        """
        Support Boolean comparison for items worn by Character.

        Returns:
            Boolean: True if items worn, False if no items worn.

        Returned if:
            if obj.clothing
        """
        return item in self.obj.db.clothing
        
    def valid_position(self, position):
        """
        Check if position is valid.
        
        Return True/False
        """
        clothing = self.obj.db.clothing
        
        position = int(position)
        
        if position > 0 and position <= len(clothing):
            return True
        else:
            return False
        
    def add(self, item, position = None, quiet=False):
        """
        Add item to Clothing list.

        Returned if:
            obj.clothing.add(item, 3)
        """
        clothing = self.obj.db.clothing

        if item in clothing:
            self.remove(item, quiet=True)

        # Sanitise position
        if position:
            position = 0 if position < 0 else position
            position = len(self) if position > len(self) else position

        # Add item to Clothing list
        if position:
            clothing.insert(position, item)
        else:
            clothing.append(item)
        
        # Telegraph
        if not quiet:
            self.obj.location.msg_contents("$You() put on $you(item).", from_obj=self.obj, mapping={"item": item})

    def remove(self, item=None, position=None, quiet=False):
        """
        Remove item from Clothing list.

        Returned if:
            obj.clothing.remove(item)
        """
        clothing = self.obj.db.clothing
        
        if position:
            del clothing[position]
        elif item:
            clothing.remove(item)

        # Telegraph
        if not quiet:
            self.obj.location.msg_contents("$You() take off $you(item).", from_obj=self.obj, mapping={"item": item})

# CLOTHING COMMANDS -----------------------------------------------------------

class CmdWear(COMMAND_DEFAULT_CLASS):
    """
    Wear an item in your inventory. Optionally, choose the position that the
    clothing is displayed in your clothing description.

    Usage:
      wear <obj> [= position]

    Examples:
      wear red shirt
      wear blue hat = 2

    All the clothes you are wearing are appended to your description.
    If you provide a 'position' after the command, the clothing will be 
    displayed in that position. i.e. the blue hat will be displayed second.
    """

    key = "wear"
    help_category = "clothing"

    def func(self):
        caller = self.caller
        args = self.args
        
        # No arguement given, prompt caller
        if not args:
            self.caller.msg("Usage: wear <obj> [=] [position e.g. 5]")
            return
        
        # Get Target
        clothing = caller.search(self.lhs, candidates=self.caller.contents)
        if not clothing:
            # No target msg handled by .search()
            return
        
        # Get position
        if self.rhs:
            if self.rhs.isdigit():
                position = self.rhs
            else:
                self.caller.msg("Usage: wear <obj> [=] [position e.g. 5]")
                return

        caller.clothing.add(clothing, position)

class CmdRemove(COMMAND_DEFAULT_CLASS):
    """
    Remove an item in your inventory by name or position.

    Usage:
      remove <obj or position>

    Examples:
      remove red shirt
      remove 2
    """

    key = "remove"
    help_category = "clothing"

    def func(self):
        caller = self.caller
        args = self.args
        
        # No arguement given, prompt caller
        if not args:
            self.caller.msg("Usage: remove <obj or position>")
            return
        
        # If given position, remove clothing at position or prompt caller
        position = args
        if position.isdigit():
            if caller.clothing.valid_position(position):
                caller.clothing.remove(position=position)
                return
            else:
                self.caller.msg("Usage: Position must be between 1 and {}".format(len(caller.clothing)))
                return
        
        # If given clothing, remove clothing or prompt caller
        clothing = caller.search(args, candidates=self.caller.clothing.list)
        if not clothing:
            # No target msg handled by .search()
            return
        caller.clothing.remove(item=clothing)
        
# CLOTHING TESTS -----------------------------------------------------------

import unittest

from evennia import create_object
from evennia.utils.test_resources import EvenniaCommandTest
from evennia.utils.utils import inherits_from

class Clothing_Tests(EvenniaCommandTest):
    """
    Test Objects:
        .account - A fake Account named “TestAccount”.
        .account2 - A fake Account named “TestAccount2”.
        .char1 - A Character linked to .account, named Char.
        .char2 - A Character linked to .account2, named Char2.
        .obj1 - A regular Object named “Obj”.
        .obj2 - Another object named “Obj2”.
        .room1 - A Room named “Room”. Both characters and objects are inside. 
                 It has a description of “room_desc”.
        .room2 - A Room named “Room2”. It is empty and has no set description.
        .exit - An exit named “out” that leads from .room1 to .room2.
        .script - A Script named “Script”. It’s an inert script.
        .session - A fake Session that mimics a player connecting to the game. 
                   It is used by .account1 and has a sessid of 1.
        
        .call() - a method for testing Evennia Commands. It allows you to compare 
                  what the command returns to the player with what you expect.
    
    Test Functions:
        .assertEqual - 
        .assertTrue - 
    """
    
    def test_ClothingCharacterMixin(self):
        # Check ClothingCharacterMixin connected.
        self.assertTrue(inherits_from(self.char1, ClothingCharacterMixin))
        
        # Check Attribute Created.
        self.assertEqual(self.char1.db.clothing, [])
        
    def test_ClothingHandler(self):
        # Check char1.clothing.list
        self.assertEqual(self.char1.clothing.list, [])
        
        # Check len(char1.clothing)
        self.assertEqual(len(self.char1.clothing), 0)
        
        # Check bool(char1.clothing)
        # Check x in char1.clothing
        # Check valid_position()
        # Check add()
        # Check remove()
    
    def test_Cmds(self):
        self.obj1.location = self.room1
        
        # Wear object not in inventory, return no find.
        self.call(CmdWear(), "Obj", "Could not find")
        
        # Wear object in inventory, return success.
        self.obj1.location = self.char1
        self.call(CmdWear(), "Obj", "You put on")
        
        # Wear object already worn, return success.
        self.call(CmdWear(), "Obj", "You put on")
       
        # Wear object with invalid position, put to end.
       
        # Wear with given position should return success.
       
        # Wear with out of bound position, return prompt.
        
        # Remove object not in inventory, return prompt.
        self.call(CmdRemove(), "Obj2", "Could not find")
       
        # Remove un-worn object in inventory, return prompt.
        self.obj2.location = self.char1
        self.call(CmdRemove(), "Obj2", "Could not find")
       
        # Remove clothing in non-valid position, return prompt.
        self.call(CmdRemove(), "10", "Usage: Position")
       
        # Remove worn object in inventory should return success.
        self.call(CmdRemove(), "Obj", "You take off")