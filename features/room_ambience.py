"""
Ambience

This is a script for sending intermittent messages to players in a room to 
provide ambiance. Messages are collected from the room and it's contents. One
message is selected to display to the player.

VARIABLES:
    obj.db.ambient_msgs = {"message":weight,..}

INSTALATION:
    1. Have Object typeclass inherit from AmbientObjectMixin()
        from features.room_ambience import AmbientObjectMixin
        class Object(AmbientObjectMixin, DefaultObject):
            pass

    2. Have Character typeclass inherit from AmbientChararacterMixin()
        from features.room_ambience import AmbientChararacterMixin
        class Character(AmbientChararacterMixin, DefaultCharacter):
            pass

    3. Have Room typeclass inherit from AmbientRoomMixin()
        from features.room_ambience import AmbientRoomMixin
        class Room(AmbientRoomMixin, DefaultRoom):
            pass
    
    4. Set up Global Script in Settings.py
        GLOBAL_SCRIPTS = {
            'key': {'AmbientScript': 'features.room_ambience',
                    'repeats': -1, 'interval': 120, 'desc': 'Triggers ambient messages in rooms from contents.'},
            }

USE:
    room.db.ambient_msgs = {}
    room.db.ambient_msgs["Ambient Message 1"] = 1
    room.db.ambient_msgs["Ambient Message 2"] = 1
    
    @py here.display_ambient_msg() # Should return "Ambient Message 1"

TO DO:
- No repeats
- Ambience messages are tagged
- Switch to not return ambient_msgs
- Add origin to ambient messages
- In-game buliding commands
"""

from evennia import DefaultObject, DefaultCharacter, DefaultRoom, DefaultScript
from evennia import TICKER_HANDLER as tickerhandler
import random
from evennia.server.sessionhandler import SESSIONS

# -----------------------------------------------------------------------------
# Ambient Message Storage
# -----------------------------------------------------------------------------


class AmbientObjectMixin():
    """
    Basic Mixin for the Ambient Objects.
    
    Adds Database Attributes:
        ambient_msgs (dict): Dict of ambient message strings and weighting. 
                             Eg. {"The sun shines brightly": 1}
    """

    def return_ambient_msgs(self):
        """
        In the basic typeclass, merely returns the raw ambient_msgs dictionary.
        """
        msgs = self.db.ambient_msgs
        return msgs if msgs else {}

class AmbientChararacterMixin():
    """
    Game specific Mixin for the Ambient Character.
    
    Ambient messages are collected from:
        -the character
        -characters equipment
        -characters junctions
    
    Adds Database Attributes:
        ambient_msgs (dict): Dict of ambient message strings and weighting. 
                             Eg. {"The sun shines brightly": 1}
    """
        
    def return_ambient_msgs(self):
        """
        Collects the ambient messages from the characters worn equipment and 
        adds them to the characters own messages
        """
        msgs = self.db.ambient_msgs
        # Append equipment messages here.
        # Append junction messages here.
        return msgs if msgs else {}


class AmbientRoomMixin():
    """
    Typeclass for the Ambient Room.
    
    Database Attributes:
        ambient_msgs (dict): Dict of ambient message strings and weighting. 
                             Eg. {"The sun shines brightly": 1}
    """

    def return_ambient_msgs(self):
        """
        Collects the ambient messages from room contents and 
        adds them to the Rooms own messages.
        """
        msgs = self.db.ambient_msgs 
        msgs = msgs if msgs else {}
        for obj in self.contents_get():
            try:
                msgs.update(obj.return_ambient_msgs())
            except:
                continue
        return msgs

    def display_ambient_msg(self, target = None):
        """
        Displays an ambient message selected at random from list returned by
        return_ambient_msgs().
        """
        msgs = self.return_ambient_msgs()
        if msgs:
            # If single target, message target only.
            if target:
                target.msg(random.choices(list(msgs.keys()), 
                                          weights=list(msgs.values()),
                                          k=1)[0])
                return
            # Otherwise mesage whole room.
            self.msg_contents(random.choices(list(msgs.keys()), 
                                             weights=list(msgs.values()),
                                             k=1)[0])

# -----------------------------------------------------------------------------
# Ambient Message Triggers
# -----------------------------------------------------------------------------

class AmbientScript(DefaultScript):
    """
    This is a Global Script. At each interval it collects a list of rooms
    which contains players. It then displays an ambiance message to it's
    contents selected from the messages returned by it's return_ambient_msgs
    function.
    """
    def at_script_creation(self):
        self.key = "ambiance_script"
        self.desc = "Triggers ambient messages in rooms from contents."
        self.interval = 120
        self.persistent = True

    def at_repeat(self):
        """
        Called every self.interval seconds.
        """
        # Get puppets with online players connected (and thus have a location)
        online_chars = [session.puppet for session in SESSIONS
                        if session.puppet]

        # Get puppet locations with no repeats
        inhabited_rooms = list(set([puppet.location for puppet in online_chars]))

        # Message room with random ambient message
        for room in inhabited_rooms:
            try:
                room.display_ambient_msg()
            except:
                continue