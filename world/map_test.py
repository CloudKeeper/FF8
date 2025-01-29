from evennia import create_object, create_script
from typeclasses import objects, rooms, exits, characters
from features import world_map
from evennia.contrib.grid import wilderness

# WORKS
# wilderness.create_wilderness(mapprovider=map_overland.PyramidMapProvider())
# wilderness.enter_wilderness(caller, coordinates=(4, 1))

wilderness.create_wilderness(name="Test", mapprovider=world_map.WorldMapProvider())
wilderness.enter_wilderness(caller, coordinates=(42, 8), name="Test")
