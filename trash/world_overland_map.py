"""
Overland Map - a Wilderness Contrib MapProvider

"""

from features import system_wilderness
from evennia import DefaultExit
from evennia.utils import evform

game_map = """\
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈≈≈≈≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈ ╭──╮__≈≈≈≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈/░░░╭──╯≈≈≈≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋/∧∧\≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈│░░/≈≈≈≈≈≈≋≋
≋≋≋≋≋≋≋≋≋≋≋_______≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋_/∧∧∧∧\_╭───╮__≈≈≈≈≈≈≈≈≈≈≈≈≈≈│░(≈≈≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋\∧∧∧∧∧∧\__≋≋≋____≋≋≋≋/∧∧∧∆∧∧∧∧∧∧∧∧∧∧∧∧\____╭───╮≈≈≈≈≈\░\≈≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋/∧∧∆∧∧∧∧∧∧\_/∧∧∧∧\≋≋(∧∧∧∧∧∧∧∩░░░░░░░░∩∧∧∧∧∧∧∧∧∧│≈≈≈≈≈≈)░)≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋/∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧\__/∧∧∧∧∩░░░░░░░░░░░↑↑↑░░░∩∧∧│≈()≈≈/░/≈≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋/∧∧∩∩∩∩∩∩∩░↑↑░░░░∧∧∧∧∧∧∧∧∩∩∩░░░░░@░░░░░↑↑↑↑↑↑░░∩∧│≈≈≈≈│░/≈≈≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋\ ░░░░░░░░↑↑↑↑↑░░░░░░░░░░░░░░░░░░║░░░░░↑↑↑↑░░░░ /∼∼≈≈≈≈/≈≈_≈≈≈≋≋≋≋
≋≋────────╯░░░░/░░░░↑↑↑░░╔════════╗░░░░░░░║░░░░░░░░░░░ /∼∼∼≈__≈≈≈≈(░)≈≈≈≋≋≋
≋≋\_ ░░░░░░░__/░░░╔══════╝↑↑↑↑↑↑↑↑╚═══════╝░░_╭───────╯∼∼≈≈(░░)≈≈≈≈≈≈≈≈≋≋≋≋
≋≋≋≋\ ░░░│═══════░║░___░░░░░↑↑↑↑↑░░░░░░░░░░░/≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋\_░░░░░░ /≋≋\@/≋≈≈\░░░░░░░░░░░░░░░░░/≈≈≈≈≈___≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋\____/≋≋≋≋≋≋≋≋≈≈≈\░░░░░░░░░░░∵∷∷∵∼≈≈___/↑↑↑)≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈∼∵░∷∵∵∵∵∷∷∷∵∼∼∼∼≈≈(░░░░░/≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈∼∵∼∼∼∼∼∼∼∼∼≈≈≈≈≈≈≈ ─── ≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈∼≈≈≈≈≈≈≈≈≈≈≋≋≋≋≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
"""
game_map_rows = game_map.splitlines()

# MAP DISPLAY METHODS #########################################################

def get_position_graphic(coordinates):
    """
    Returns character at coordinates in World Map.
    
    Args:
        Coordinates: Tuple of Ints (x, y)
    
    Returns:
        String: The character at the provided coordinates in World Map.
    
    """
    x, y = coordinates
    yaxis = game_map_rows[y % len(game_map_rows)]
    char = yaxis[x % len(yaxis)]
    return char

def get_minimap(coordinates, mapsize):
    """
    Returns minimap surrounding given coordinates.

    Args:
        Coordinates: Tuple of Ints (x, y) for location on map
        mapsize: Tuple of Ints (x, y) for size of minimap returned

    Returns:
        String: A square map of xsize and ysize with the coordinates in the
                centre.
    """
    x, y = coordinates
    xsize, ysize = mapsize
    line = ""
    minimap = []
    
    for row in range(int(y-(ysize-1)/2), int(y+(ysize-1)/2)+1):
        for column in range(int(x-(xsize-1)/2), int(x+(xsize-1)/2)+1):
            line = line + get_position_graphic((column,row))
        minimap.append(line)
        line = ""
    
    minimap = "\n".join(minimap)
    return minimap

# MAP ENTRANCE ################################################################

# class OverlandEntrance(DefaultExit):
#     """
#     This is an Exit object used outside the World Map. A player uses it to
#     enter into the Overland Map at the coodinates of the Exit's location.
#     """

#     def at_traverse(self, traversing_object, target_location):
#         """
#         This implements the actual traversal. The traverse lock has
#         already been checked a (in the Exit command) at this point.

#         Args:
#             traversing_object (Object): Object traversing us.
#             **kwargs (dict): Arbitrary, optional arguments for users
#                 overriding the call (unused by default).
#         """
#         world_map = GLOBAL_SCRIPTS.world_map
#         # coordinates = self.location.attributes.get("coordinates")
#         coordinates = (51,290)

#         if world_map.is_valid_coordinates(coordinates):
#             world_map.move_obj(traversing_object, coordinates)
#             return True
#         else:
#             return False

# MAP EXIT ####################################################################

# class OverlandExit(system_wilderness.WildernessExit):
#     """
#     This is an Exit object used inside a WildernessRoom. Instead of changing
#     the location of an Object traversing through it (like a traditional exit
#     would do) it changes the coordinates of that traversing Object inside
#     the wilderness map.
#     """

#     def at_traverse_coordinates(self, traversing_object, current_coordinates, new_coordinates):
#         """
#         Called when an object wants to travel from one place inside the
#         wilderness to another place inside the wilderness.

#         If this returns True, then the traversing can happen. Otherwise it will
#         be blocked.

#         This method is similar how the `at_traverse` works on normal exits.

#         Args:
#             traversing_object (Object): The object doing the travelling.
#             current_coordinates (tuple): (x, y) coordinates where
#                 `traversing_object` currently is.
#             new_coordinates (tuple): (x, y) coordinates of where
#                 `traversing_object` wants to travel to.

#         Returns:
#             bool: True if traversing_object is allowed to traverse
#         """
#         return True

# MAP PROVIDER ################################################################

# class OverlandMapProvider(system_wilderness.WildernessMapProvider):
#     """
#     Default Wilderness Map provider.

#     This is a simple provider that just creates an infinite large grid area.
#     """
    
    # room_typeclass = system_wilderness.WildernessRoom
    # exit_typeclass = system_wilderness.WildernessExit

    # def is_valid_coordinates(self, wilderness, coordinates):
    #     """
    #     Returns True if coordinates is valid and can be walked to.

    #     Args:
    #         wilderness: the wilderness script
    #         coordinates (tuple): the coordinates to check as (x, y) tuple.

    #     Returns:
    #         bool: True if the coordinates are valid
    #     """

    #     x, y = coordinates
    #     if x < 0:
    #         return False
    #     if y < 0:
    #         return False

    #     return True

    # def get_location_name(self, coordinates):
    #     """
    #     Returns a name for the position at coordinates.

    #     Args:
    #         coordinates (tuple): the coordinates as (x, y) tuple.

    #     Returns:
    #         name (str)
    #     """

    #     return "Balamb"

    # def at_prepare_room(self, coordinates, caller, room):
    #     """
    #     Called when a room gets activated for certain coordinates. This happens
    #     after every object is moved in it.
        
    #     This can be used to set a custom room desc for instance or run other
    #     customisations on the room.

    #     Args:
    #         coordinates (tuple): the coordinates as (x, y) where room is
    #             located at
    #         caller (Object): the object that moved into this room
    #         room (WildernessRoom): the room object that will be used at that
    #             wilderness location
    #     Example:
    #         An example use of this would to plug in a randomizer to show different
    #         descriptions for different coordinates, or place a treasure at a special
    #         coordinate.
    #     """
        
    #     FORM = """\
    #     ─ cAcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc ─
    #     ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    #     ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    #     ccBcc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    #     ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    #     ccccc │ cccccccccccccccccCcccccccccccccccccccccccccccccccccccccccccccccccccccc
    #     """

    #     name = str(coordinates)
    #     A = name + " " + "─"*(76-len(name))
    #     B = get_minimap(coordinates, (5,5))
    #     C = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        
    #     form = evform.EvForm({"FORM": FORM, "TABLECHAR": "x", "FORMCHAR": "c"})
    #     form.map(cells={"A":A, "B":B, "C":C})

    #     room.ndb.active_desc = str(form)

from evennia.contrib.grid import wilderness

map_str = '''
     .
    ...
   .....
  .......
'''

class PyramidMapProvider(wilderness.WildernessMapProvider):

    def is_valid_coordinates(self, wilderness, coordinates):
        "Validates if these coordinates are inside the map"
        x, y = coordinates
        try:
            lines = map_str.split("\n")
            # The reverse is needed because otherwise the pyramid will be
            # upside down
            lines.reverse()
            line = lines[y]
            column = line[x]
            return column == "."
        except IndexError:
            return False

    def get_location_name(self, coordinates):
        "Set the location name"
        x, y = coordinates
        if y == 3:
            return "Atop the pyramid."
        else:
            return "Inside a pyramid."

    def at_prepare_room(self, coordinates, caller, room):
        "Any other changes done to the room before showing it"
        x, y = coordinates
        desc = "This is a room in the pyramid."
        if y == 3 :
            desc = "You can see far and wide from the top of the pyramid."
        room.ndb.active_desc = desc