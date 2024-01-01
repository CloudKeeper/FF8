
from evennia import create_object
from typeclasses import rooms, exits, characters

# INITIATE ROOMS

room1 = create_object(rooms.Room, key="Room 1")
room2 = create_object(rooms.Room, key="Room 2")

# ROOM 1 DETAILS

room1.db.desc = ("Description for Room1")

room1.db.details = {}
room1.db.details["detail"] = ("Test Detail")

room1.db.ambient_msgs = {}
room1.db.ambient_msgs["Ambient Message 1"] = 1
room1.db.ambient_msgs["Ambient Message 2"] = 1
room1.db.ambient_msgs["Ambient Message 3"] = 1

room1_exit = create_object("typeclasses.exits.Exit", key="Room 2", location=room1, destination=room2)
room1_exit.db.delay = 5

# ROOM 2 DETAILS

room2.db.desc = ("Description for Room2")

room2.db.details = {}
room2.db.details["detail"] = ("Test Detail")

room2.db.ambient_msgs = {}
room2.db.ambient_msgs["Ambient Message 1"] = 1
room2.db.ambient_msgs["Ambient Message 2"] = 1
room2.db.ambient_msgs["Ambient Message 3"] = 1

room2_exit = create_object("typeclasses.exits.Exit", key="Room 1", location=room2, destination=room1)
room2_exit.db.delay = 0

caller.location = room1