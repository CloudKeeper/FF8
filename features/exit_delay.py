"""
Delayed Exit
This is an Exit mixin which delays a character leaving after using the exit.
If a player stops or poses whilst leaving, it stops the exit process.

INSTALLATION:
1. Have Exit typeclass inherit from DelayedExitMixin()
    from features.exit_delay import DelayedExitMixin
    class Exit(DelayedExitMixin, DefaultExit):
        pass

USE:
    room1_exit = create_object("typeclasses.exits.Exit", key="North", location=room1, destination=room2)
    room1_exit.db.delay = 5

TO DO:
-Use get_display_name
"""

from evennia import DefaultExit
from evennia import utils

class DelayedExitMixin(DefaultExit):
    """
    This is an Exit mixin which delays a character leaving after using the exit.
    If a player stops or poses whilst leaving, it stops the exit process.
    
    """

    def at_traverse(self, traversing_object, target_location):
        """
        This implements the actual traversal, using utils.delay to delay the 
        move_to() call. The traverse lock has already been checked (in the Exit 
        command) at this point.

        Args:
            traversing_object: (Object) Object traversing us.
            target_location:   (Object) Where target is going.
            **kwargs:          (dict) Arbitrary, optional arguments for users
                               overriding the call (unused by default).
        
        Attributes - Used if available:
            delay:                 (INT) Defines the delay (default - 5s)
            traversing_object_msg: (String) Response to exit command - Can use 'source', exit', 'destination', 'player' .format args
            traversing_object_pose:(String) Pose given to exiting object - Can use 'source', 'exit', 'destination', 'player' .format args
            room_leave_msg:        (String) Message to room on exit command - Can use 'source', 'exit', 'destination', 'player' .format args
            err_traverse:          (String) Message if traverse fails after delay
        
        Delayed_exit contrib uses traversing_object.ndb.destination as check.
        We use pose, so stop command will cover both posing and exiting.
        """

        # Prepare traversal messages.
        traversing_object_msg = self.attributes.get("traversing_object_msg", 
                                default = "You begin leaving {source}, heading for {destination}.")\
                                .format(source = traversing_object.location, \
                                        exit = self.name, \
                                        destination = target_location.name, \
                                        player = traversing_object.name)
        
        room_leave_msg = self.attributes.get("room_leave_msg", 
                         default = "{player} begins leaving {source}, heading for {destination}.")\
                         .format(source = traversing_object.location, \
                                 exit = self.name, \
                                 destination = target_location.name, \
                                 player = traversing_object.name)

        # Telegraph traversal messages.
        traversing_object.msg(traversing_object_msg)
        traversing_object.location.msg_contents(room_leave_msg, exclude=traversing_object)
        
        # Would normally be 'traversing_object.ndb.currently_moving = True'
        # Synergy with Pose system - Set up pose to check after delay.
        traversing_pose = self.attributes.get("traversing_object_pose", 
                          default = " is leaving {source}, heading for {destination}.")\
                          .format(source = traversing_object.location, \
                                  exit = self.name, \
                                  destination = target_location.name, \
                                  player = traversing_object.name)
        traversing_object.db.pose = traversing_pose
        
        # Set up delay duration
        delay = self.attributes.get("delay", default = 0)
        
        # Set up Callback function for after delay.
        def traverse_callback():
            """
            This callback will be called by utils.delay after self.db.delay 
            seconds, completing the actual movement.
            """
            # Would normally be 'if not traversing_object.ndb.currently_moving:'
            # Synergy with Pose system - If leaving pose has been stopped or interrupted, kill movement.
            if not traversing_object.db.pose == traversing_pose:
                return
            
            # Otherwise deal with movement.
            source_location = traversing_object.location
            if traversing_object.move_to(target_location, 
                                         msg="{object} left {origin}, heading for {destination}."):
                 self.at_after_traverse(traversing_object, source_location)
            else:
                # Use exit's error message if it exists, or default message.
                traversing_object.msg(self.attributes.get("err_traverse",
                            default = "You cannot go there."))

        # Trigger delay
        utils.delay(delay, callback=traverse_callback)