"""
Drawpoints

This is an Object and Command for collecting magic from a room.

In FF8, every 10,240 steps gave a 50% to recharge a draw point one step. At
4 steps a second, that's 2560 seconds or 42.67 minutes. Draw points were
empty, partially charged, or fully charged. They returned:
    IN LOCATION
        6-15 if rich and fully stocked
        3-8 if rich and partially stocked
        3-8 if not rich and fully stocked
        2-4 if not rich and partially stocked
    
    ON MAP
        2-5 if rich
        1-2 if not rich

REQUIREMENT:
    - Characters must have the magic handler installed.
    - (Optional) Ambience System

INSTALATION:
    1. Grant the Character with the CmdDraw()
        from features.object_drawpoint import CmdDraw
        
        class CharacterCmdSet(default_cmds.CharacterCmdSet):
            key = "DefaultCharacter"
            def at_cmdset_creation(self):
                super().at_cmdset_creation()
                self.add(CmdDraw)

USE:
    create Drawpoint:features.object_drawpoint.Drawpoint
    draw

"""

import time
import random
from evennia import search_tag
from typeclasses.objects import Object
from django.conf import settings
from evennia.utils import utils

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


class Drawpoint(Object):
    """
    An invisible object from which magic can be drawn from.
    
    Attributes:
        magic    (String): Name of the magic that can be drawn. Eg. "Fire"
        draw_level  (Int): The stage of magic to be drawn.
        last_draw (float): The time the point was last drawn from.
        recharge_rate   (Int): Rate that draw_level increases.
        draw_info  (List): Contains a Dictionary for each draw_level.
                           [{"draw_rate":(0,0), "draw_msg":"", "ambience_msg":{}}]
    """
    
    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.
        """
        super(Drawpoint, self).at_object_creation()
        
        # Set drawpoint tag
        self.tags.add("drawpoint")
        
        # Set invisibility
        self.locks.add("search:false()")
        
        # Set defaults
        self.db.magic = "Thunder"
        self.db.draw_level = 0
        self.db.last_draw = time.time()
        self.db.recharge_rate = 2560
        self.db.draw_info = [
            
            {"draw_rate":(0,0), 
             "draw_msg":"There is nothing to draw here.", 
              "ambience_msgs":{"Level 0":1}},
              
            {"draw_rate":(3,8), 
             "draw_msg":"A swirl of energy enters {caller}.", 
              "ambience_msgs":{"Level 1":1}},
              
            {"draw_rate":(6,15), 
             "draw_msg":"A swirl of energy enters {caller}.", 
              "ambience_msgs":{"Level 2":1}}
        ]
        
        
    def recharge_point(self):
        """
        Calculate the current draw_level.
        
        """
        # If at max draw_level, return
        draw_level = self.db.draw_level
        draw_info = self.db.draw_info
        if len(draw_info) == draw_level:
                return
        
        # If not at max draw_level, recharge point
        seconds_from_last_draw = time.time() - self.db.last_draw
        no_of_recharges, remainder = divmod(seconds_from_last_draw, self.db.recharge_rate)
        
        for recharge in range(int(no_of_recharges)):
            draw_level += random.randint(0, 1)
            if len(draw_info) == draw_level:
                break

        # Respsect remaining time until next recharge
        self.db.last_draw = time.time()-remainder
        return


    def at_draw(self, caller):
        """
        Called by the CmdDraw command, this implements draw functionality. 

        Args:
            caller: (Object) Object drawing from the Drawpoint.
        
        """
        self.recharge_point()
        
        # If not charged, return
        draw_level = self.db.draw_level
        draw_info = self.db.draw_info
        if not draw_level:
            caller.msg(draw_info[draw_level]["draw_msg"].format(caller=caller, 
                                                                location=caller.location, 
                                                                drawpoint=self.get_display_name(caller)))
            return
        
        # Send optional descriptive message to caller and location
        draw_msg = draw_info[draw_level]["draw_msg"]
        if draw_msg:
            caller.msg(draw_msg.format(caller="you", 
                                       location=caller.location, 
                                       drawpoint=self.get_display_name(caller)))
            caller.location.msg_contents(draw_msg.format(caller=caller.get_display_name(), 
                                                         location=caller.location, 
                                                         drawpoint=self.get_display_name(caller)), 
                                                         exclude=[caller])
        
        # Give caller Magic.
        magic = self.db.magic
        draw_rate =  draw_info[draw_level]["draw_rate"]
        magic_amount = random.randint(draw_rate[0], draw_rate[1])
        draw_successful = caller.magic.add(magic, magic_amount) 
        # Messaging player is handled by caller.magic.add
        
        # Reset drawpoint
        if draw_successful:
            self.db.draw_level = 0
            self.db.last_draw = time.time()
        return

    def return_ambience_msgs(self):
        """
        Functionality for the Ambience Messsage system.
        
        Attributes - Used if available:
            draw_level:  (Int) Defines the amount of magic to be drawn.
            draw_info  (List): Contains a Dictionary for each draw_level.
                               [{"draw_rate":(0,0), "draw_msg":"", "ambience_msgs":{}}]
        
        Returns:
            msgs (dictionary): String and int indicating the ambience message and
                               it's weight. Eg. {"The sun shines brightly": 1}
        """
        self.recharge_point()
        
        msgs = self.db.draw_info[self.db.draw_level]["ambience_msgs"]
        return msgs


class CmdDraw(COMMAND_DEFAULT_CLASS):
    """
    Draw magic from a drawpoint at your location.
    
    Usage:
        draw
        
    """
    key = "draw"
    locks = "cmd:all()"

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the cmdhandler right after self.parser() finishes, and so has access
        to all the variables defined therein.
        """
        caller = self.caller
        
        # Check if a draw point is at the location.
        # drawpoint = caller.search("drawpoint", quiet=True, use_locks=False)
        drawpoint = search_tag("drawpoint").filter(db_location=caller.location)
        
        # If no draw point, inform caller.
        if not drawpoint:
            caller.msg("There is nothing to draw here.")
            return
           
        # If draw point, infom caller and trigger draw.
        caller.msg("Found a draw point! {} found.".format(drawpoint[0].db.magic))
        drawpoint[0].at_draw(caller)