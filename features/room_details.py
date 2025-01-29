"""
Details
This is a Room mixin and command to implement Room Detials. Details are 
non-object descriptions stored on the room which a player can look at to 
recieve a more detailed description.

VARIABLES:
    obj.db.details = {"detail name":"detail message",..}

INSTALLATION:
1. Have Room typeclass inherit from DetailRoomMixin
    from features.room_details import DetailRoomMixin
    class Room(DetailRoomMixin, DefaultRoom):
        pass
        
2. Ovverride the vanilla look command with the CmdDetailLook()
    from features.room_details import CmdDetailLook
    
    class CharacterCmdSet(default_cmds.CharacterCmdSet):
        key = "DefaultCharacter"
        def at_cmdset_creation(self):
            super().at_cmdset_creation()
            self.add(CmdDetailLook)

USE:
    room.db.details = {}
    room.db.details["detail"] = ("Test Detail")
    
    >look detail # Should return "Test Detail"
"""

from evennia import utils, DefaultRoom, CmdSet, default_cmds
from django.conf import settings
_SEARCH_AT_RESULT = utils.object_from_module(settings.SEARCH_AT_RESULT)

class DetailRoomMixin():
    """
    This is a mixin that provides object functionality for details.
    """

    def return_detail(self, detailkey):
        """
        This looks for an Attribute "obj_details" and possibly
        returns the value of it.
        Args:
            detailkey (str): The detail being looked at. This is
                case-insensitive.
        """
        details = self.db.details
        if details:
            return details.get(detailkey.lower(), None)

class CmdDetailLook(default_cmds.CmdLook):
    """
    Observes your location or details at your location or objects
    in your vicinity.
    
    Usage:
        look
        look <obj>
        look <room detail>
        look *<account>
    """

    def func(self):
        caller = self.caller
        args = self.args
        
        # No arguement given - returns room's description.
        if not args:
            target = [caller.location]
            # If no room, give error.
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            # Check if argument matches an object with search()
            target = caller.search(self.args, use_nicks=True, quiet=True)
        
        # If no target found - check if argument matches a detail.
        if not target:
            # Search for details.
            detail = caller.location.return_detail(args)
            if detail:
                self.msg((detail, {"type": "look"}), options=None)
                return
            # If no details - trigger default NO_MATCH behaviour.
            _SEARCH_AT_RESULT(target, caller, args)
            return

        # If multiple targets - trigger default MULTI_MATCH behaviour.
        if len(target) > 1:
            _SEARCH_AT_RESULT(target, caller, args)
            return
        
        # If one target - return appearance.
        if target:
            self.msg((caller.at_look(target[0]), {"type": "look"}), options=None)