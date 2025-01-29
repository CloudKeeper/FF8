"""
TODO:
- Put X at Centre of the mini map
- Remove unneeded name from Form
- Limit movement
- Set up Dummy world map with pre-built coordinate locations
- Correct movement directions
"""

from evennia.contrib.grid import wilderness
from evennia.utils import evform

game_map = """\
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈≈≈≈≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈╭──╮__≈≈≈≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈/░░░╭──╯≈≈≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋/∧∧\≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈│░░/≈≈≈≈≈≋≋≋
≋≋≋≋≋≋≋≋≋≋≋_______≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋_/∧∧∧∧\_╭───╮__≈≈≈≈≈≈≈≈≈≈≈≈≈≈│░(≈≈≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋\∧∧∧∧∧∧\__≋≋≋____≋≋≋≋/∧∧∧∆∧∧∧∧∧∧∧∧∧∧∧∧\____╭───╮≈≈≈≈≈\░\≈≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋/∧∧∆∧∧∧∧∧∧\_/∧∧∧∧\≋≋(∧∧∧∧∧∧∧∩░░░░░░░░∩∧∧∧∧∧∧∧∧∧│≈≈≈≈≈≈)░)≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋/∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧∧\__/∧∧∧∧∩░░░░░░░░░░░↑↑↑░░░∩∧∧│≈()≈≈/░/≈≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋/∧∧∩∩∩∩∩∩∩░↑↑░░░░∧∧∧∧∧∧∧∧∩∩∩░░░░░@░░░░░↑↑↑↑↑↑░░∩∧│≈≈≈≈│░/≈≈≈≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋\ ░░░░░░░░↑↑↑↑↑░░░░░░░░░░░░░░░░░░║░░░░░↑↑↑↑░░░░ /≈≈≈≈≈≈/≈≈_≈≈≈≋≋≋≋
≋≋────────╯░░░░/░░░░↑↑↑░░╔════════╗░░░░░░░║░░░░░░░░░░░ /≈≈≈≈__≈≈≈≈(░)≈≈≈≋≋≋
≋≋\_ ░░░░░░░__/░░░╔══════╝↑↑↑↑↑↑↑↑╚═══════╝░░_╭───────╯≈≈≈≈(░░)≈≈≈≈≈≈≈≈≋≋≋≋
≋≋≋≋\ ░░░│═══════╗║░___░░░░░↑↑↑↑↑░░░░░░░░░░░/≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋\_░░░░░░ /≋≋\@/≈≈≈\░░░░░░░░░░░░░░░░░/≈≈≈≈≈___≈≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋\____/≋≋≋≋≋≋≋≋≈≈≈\░░░░░░░░░░░∵∷∷∵≈≈≈___/↑↑↑)≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈∵░∵∷∷∷∷∷∷∷∵≈≈≈≈≈≈(░░░░░/≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈∵≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ ─── ≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≋≋≋≋≈≈≈≈≈≈≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋
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
    
    # Ensure minimap always has a centre character
    xsize, ysize = mapsize
    xsize = xsize if xsize % 2 == 1 else xsize -1
    ysize = ysize if ysize % 2 == 1 else ysize -1
    line = ""
    minimap = []
    
    # Build MiniMap
    for row in range(y-ysize//2, y+ysize//2+1):
        for column in range(x-xsize//2, x+xsize//2+1):
            line = line + get_position_graphic((column,row))
        minimap.append(line)
        line = ""

    # Replace players location with 'X'
    middle = minimap[len(minimap)//2]
    minimap[len(minimap)//2]=middle[:len(middle)//2] + 'X' + middle[len(middle)//2 + 1:]

    minimap = "\n".join(minimap)
    return minimap

# MAP PROVIDER ################################################################

class WorldMapProvider(wilderness.WildernessMapProvider):

    def is_valid_coordinates(self, wilderness, coordinates):
        """
        Returns True if coordinates is valid and can be walked to.

        Args:
            wilderness: the wilderness script
            coordinates (tuple): the coordinates to check as (x, y) tuple.

        Returns:
            bool: True if the coordinates are valid
        """
        x, y = coordinates
        if x < 0:
            return False
        if y < 0:
            return False

        return True

    def get_location_name(self, coordinates):
        """
        Returns a name for the position at coordinates.

        Args:
            coordinates (tuple): the coordinates as (x, y) tuple.

        Returns:
            name (str)
        """
        
        return "Balamb"

    def at_prepare_room(self, coordinates, caller, room):
        """
        Called when a room gets activated for certain coordinates. This happens
        after every object is moved in it.
        
        This can be used to set a custom room desc for instance or run other
        customisations on the room.

        Args:
            coordinates (tuple): the coordinates as (x, y) where room is
                located at
            caller (Object): the object that moved into this room
            room (WildernessRoom): the room object that will be used at that
                wilderness location
        Example:
            An example use of this would to plug in a randomizer to show different
            descriptions for different coordinates, or place a treasure at a special
            coordinate.
        """
        FORM = \
"""\
─ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc ─
ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccAcc │ ccBccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
"""

        A = get_minimap(coordinates, (5,5))
        B = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        
        form = evform.EvForm({"FORM": FORM, "TABLECHAR": "x", "FORMCHAR": "c"})
        form.map(cells={"A":A, "B":B})

        room.ndb.active_desc = str(form)