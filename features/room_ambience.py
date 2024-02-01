"""
Ambience

This is a script for sending intermittent messages to players in a room to 
provide ambiance. Messages are collected from the room and it's contents. One
message is selected to display to the player.

VARIABLES:
    obj.db.ambience_msgs = {"message":weight,..}

INSTALATION:
    1. Have Object typeclass inherit from AmbienceObjectMixin()
        from features.room_ambience import AmbienceObjectMixin
        class Object(AmbienceObjectMixin, DefaultObject):
            pass

    2. Have Character typeclass inherit from AmbienceChararacterMixin()
        from features.room_ambience import AmbienceChararacterMixin
        class Character(AmbienceChararacterMixin, DefaultCharacter):
            pass

    3. Have Room typeclass inherit from AmbienceRoomMixin()
        from features.room_ambience import AmbienceRoomMixin
        class Room(AmbienceRoomMixin, DefaultRoom):
            pass
    
    4. Set up Global Script in Settings.py
        GLOBAL_SCRIPTS = {
            'key': {'AmbienceScript': 'features.room_ambience',
                    'repeats': -1, 'interval': 120, 'desc': 'Triggers ambience messages in rooms from contents.'},
            }

USE:
    room.db.ambience_msgs = {}
    room.db.ambience_msgs["Ambience Message 1"] = 1
    room.db.ambience_msgs["Ambience Message 2"] = 1
    
    @py here.display_ambience_msg() # Should return "Ambience Message 1"

TO DO:
- No repeats
- Ambience messages are tagged
- Switch to not return ambience_msgs
- Add origin to ambience messages
- In-game buliding commands
"""

from evennia import DefaultObject, DefaultCharacter, DefaultRoom, DefaultScript
from evennia import TICKER_HANDLER as tickerhandler
import random
from evennia.server.sessionhandler import SESSIONS

# -----------------------------------------------------------------------------
# Ambience Message Storage
# -----------------------------------------------------------------------------


class AmbienceObjectMixin():
    """
    Basic Mixin for the Ambience Objects.
    
    Adds Database Attributes:
        ambience_msgs (dict): Dict of ambience message strings and weighting. 
                             Eg. {"The sun shines brightly": 1}
    """

    def return_ambience_msgs(self):
        """
        In the basic typeclass, merely returns the raw ambience_msgs dictionary.
        
        Returns:
            msgs (dictionary): String and int indicating the ambience message and
                               it's weight. Eg. {"The sun shines brightly": 1}
        """
        msgs = {}
        msgs.update(self.attributes.get("ambience_msgs", default = {}))
        return msgs

class AmbienceChararacterMixin():
    """
    Game specific Mixin for the Ambience Character.
    
    Ambience messages are collected from:
        -the character
        -characters equipment
        -characters junctions
    
    Adds Database Attributes:
        ambience_msgs (dict): Dict of ambience message strings and weighting. 
                             Eg. {"The sun shines brightly": 1}
    """
        
    def return_ambience_msgs(self):
        """
        Collects the ambience messages from the characters worn equipment and 
        adds them to the characters own messages
        
        Returns:
            msgs (dictionary): String and int indicating the ambience message and
                               it's weight. Eg. {"The sun shines brightly": 1}
        """
        msgs = {}
        msgs.update(self.attributes.get("ambience_msgs", default = {}))
        # Append equipment messages here.
        # Append junction messages here.
        return msgs


class AmbienceRoomMixin():
    """
    Typeclass for the Ambience Room.
    
    Database Attributes:
        ambience_msgs (dict): Dict of ambience message strings and weighting. 
                             Eg. {"The sun shines brightly": 1}
    """

    def return_ambience_msgs(self):
        """
        Collects the ambience messages from room contents and 
        adds them to the Rooms own messages.
        
        Returns:
            msgs (dictionary): String and int indicating the ambience message andE
                               it's weight. Eg. {"The sun shines brightly": 1}
        """
        msgs = {}
        msgs.update(self.attributes.get("ambience_msgs", default = {}))
        for obj in self.contents_get():
            try:
                msgs.update(obj.return_ambience_msgs())
            except:
                continue
        return msgs

    def display_ambience_msg(self, target = None):
        """
        Displays an ambience message selected at random from list returned by
        return_ambience_msgs().
        """
        msgs = self.return_ambience_msgs()
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
# Ambience Message Triggers
# -----------------------------------------------------------------------------

class AmbienceScript(DefaultScript):
    """
    This is a Global Script. At each interval it collects a list of rooms
    which contains players. It then displays an ambiance message to it's
    contents selected from the messages returned by it's return_ambience_msgs
    function.
    """
    def at_script_creation(self):
        self.key = "ambiance_script"
        self.desc = "Triggers ambience messages in rooms from contents."
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

        # Message room with random ambience message
        for room in inhabited_rooms:
            try:
                room.display_ambience_msg()
            except:
                continue