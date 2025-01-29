
from evennia import create_object, create_script
from typeclasses import rooms, exits, characters
from features import world_map

# # INITIATE ROOMS

# room1 = create_object(rooms.Room, key="Room 1")
# room2 = create_object(rooms.Room, key="Room 2")

# # ROOM 1 DETAILS ##############################################################

# room1.db.desc = ("Description for Room1")

# # Details
# room1.db.details = {}
# room1.db.details["detail"] = ("Test Detail")

# # ambience Messages
# room1.db.ambience_msgs = {}
# room1.db.ambience_msgs["ambience Message 1"] = 1
# room1.db.ambience_msgs["ambience Message 2"] = 1
# room1.db.ambience_msgs["ambience Message 3"] = 1

# # Delayed Exit
# room1_exit = create_object("typeclasses.exits.Exit", key="Room 2", location=room1, destination=room2)
# room1_exit.db.delay = 5
# room1_exit.db.return_appearance_type = "destination_desc"

# # Drawpoint
# drawpoint = create_object("features.object_drawpoint.Drawpoint", key="test", location=room1)

# # NPC
# stringNPC = create_object("typeclasses.characters.NPC", key="string", location=room1)
# stringNPC.db.conversation = "String"
# stringNPC.sdesc.add("String")

# listNPC = create_object("typeclasses.characters.NPC", key="list", location=room1)
# listNPC.db.conversation = ["List1", "List2"]
# listNPC.sdesc.add("List")

# dictNPC = create_object("typeclasses.characters.NPC", key="dict", location=room1)
# dictNPC.db.conversation = ["List1", "List2"]
# dictNPC.sdesc.add("Dict")

# # ROOM 2 DETAILS ##############################################################

# room2.db.desc = ("Description for Room2")

# # Details
# room2.db.details = {}
# room2.db.details["detail"] = ("Test Detail")

# # ambience Messages
# room2.db.ambience_msgs = {}
# room2.db.ambience_msgs["ambience Message 1"] = 1
# room2.db.ambience_msgs["ambience Message 2"] = 1
# room2.db.ambience_msgs["ambience Message 3"] = 1

# # Delayed Exit
# room2_exit = create_object("typeclasses.exits.Exit", key="Room 1", location=room2, destination=room1)
# room2_exit.db.delay = 0

# caller.location = room1

# ----------------------------------

# room1 = create_object(rooms.Room, key="Room 1")
# caller.location = room1

# # world_map = create_script(key="world_map", typeclass="features.world_map.WildernessScript")

# wilderness_entrance = create_object(world_map.WildernessEntrance, key="World Map", location= room1)

# --------------------------

# caller.msg(world_map.get_minimap((289,53), (5,5)))

#  --------------------------

# from evennia.utils import evform

# FORM = \
# """ 
# ─ cAccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc─
#  ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#  ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#  ccBcc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#  ccccc │ cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#  ccccc │ cccccccccccccccccCcccccccccccccccccccccccccccccccccccccccccccccccccccc

# """

# name = "Room Name"
# A = name + " " + "─"*(76-len(name))
# B = world_map.get_minimap((289,53), (5,5))
# C = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

# form = evform.EvForm({"FORM": FORM, "TABLECHAR": "x", "FORMCHAR": "c"})
# form.map(cells={"A":A, "B":B, "C":C})

# caller.msg(form)