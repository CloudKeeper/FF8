"""
Transport

A room which moves from location to location, allowing entry and exit.

Create a camera object which allows you to use the "photograph" command. When
the "photograph" command is used, the descriptions of your listed targets 
(by default the current room and room contents) will be saved onto a newly
created photograph object and can be viewed at any time after by looking
at the photograph.

Technical:
The 'photograph' command triggers the custom use_object() function on the 
camera object. The use_object() function creates a photo object and saves 
a dictionary of object names and descriptions. The photo object has a custom
return_appearance() function that draws upon the saved description data to
create an EvMenu that emulates being at the location.

Usage - In-game:
    @create camera:features.photography.Camera
    selfie

"""

import time
from django.conf import settings
from evennia.utils import utils, evmenu
from evennia import CmdSet
from evennia.utils.create import create_object
from typeclasses.rooms import Room

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)

_TGT_ERRMSG = "'{}' could not be located."

# ------------------------------------------------------------------------------
# Camera Commands - Calls the camera.use_object() function
# ------------------------------------------------------------------------------


class TransportCmdSet(CmdSet):
    """
    Camera Command Set
    """
    key = "cameracmdset"
    priority = 1

    def at_cmdset_creation(self):
        self.add(CmdEnter())
        self.add(CmdExit())


class CmdEnter(COMMAND_DEFAULT_CLASS):
    """
    Enter the Transport.

    Usage:
        Enter
        
    This will be available to players in the same location
    as the train and allows them to embark. 
    """
    key = "enter"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Pass specified subjects to obj or default to location.contents"""

        self.caller.msg("You board the train.")
        self.caller.move_to(self.obj, move_type="board")

class CmdExit(COMMAND_DEFAULT_CLASS):
    """
    Exit the Transport.

    Usage:
        Exit
    
    This will be available to everyone inside the 
    train. It allows them to exit to the train's
    current location. 
    """
    key = "exit"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Pass specified subjects to obj or default to location.contents"""

        self.caller.msg("You exit the train.")
        self.caller.move_to(self.obj.location, move_type="disembark")

# ------------------------------------------------------------------------------
# Camera Object - Creates photographs when used.
# ------------------------------------------------------------------------------


class Transport(Room):

    def at_object_creation(self):
        self.cmdset.add_default(TransportCmdSet, permanent=True)
        super(Transport, self).at_object_creation()

    # def at_use(self, character, subjects):

    #     # Create photograph object.
    #     photo = create_object(typeclass=Photograph, location=character,
    #                           key="Photo " + character.location.key 
    #                           + str(int(time.time())))
        
    #     # Stores names and descriptions of Characters/Objects at location.
    #     photo.db.desc = "A small polaroid picture."
    #     photo.db.image = ("Captured in the glossy polaroid is: \n" +
    #                       character.location.key + "\n" +
    #                       character.location.db.desc + "\n")
    #     photo.db.subjects = {subject.key: subject.db.desc 
    #                          for subject in list(set(subjects))}
    #     character.location.msg_contents(character.key 
    #                                     + " snapped a photograph!")

# ------------------------------------------------------------------------------
# Photograph Object - Uses menus to mimic location when photograph taken.
# ------------------------------------------------------------------------------


# class Photograph(Object):

#     def return_appearance(self, looker):

#         # Initialise photograph menu.
#         evmenu.EvMenu(looker, "features.photography",
#                       startnode="photograph_node", persistent=True,
#                       cmdset_mergetype="Replace",
#                       node_formatter=photograph_node_formatter,
#                       options_formatter=photograph_options_formattter,
#                       photodesc=self.db.image, 
#                       subjects=self.db.subjects,
#                       current_state="")
#         return ""