"""
Batchcode for testing purposes.

"""

from evennia.utils import create, search

# # Create invisible object
# obj = create.create_object(key="test", location=caller.location)
# obj.locks.add("search:false()")
# obj.locks.add("view:false()")

# if obj.access(obj, 'search'):
#     caller.msg("search allowed")
# if not obj.access(obj, 'search'):
#     caller.msg("search not allowed")

# results = caller.location.contents
# if search.objects("Ben") :
#     caller.msg("Found Ben")
# for obj in [x for x in results if x.access(search.objects("Ben"), "search")]:
#     caller.msg(obj.key + " passed")

# # Testing Delayed Exit
# obj = create.create_object("typeclasses.default_typeclasses.Room", key="room", location=None)
# exit = create.create_object("features.delayed_exits.DelayedExitMixin", key="room", location=caller.location, destination=obj)
# exit.db.delay = 5
# exit2 = create.create_object("features.delayed_exits.DelayedExitMixin", key="limbo", location=obj, destination=caller.location)
# exit2.db.delay = 5

# # Testing See Through Exits
# room = create.create_object("typeclasses.default_typeclasses.Room", key="room", location=None)
# room.db.desc = "room description"
# obj = create.create_object(key="obj", location=room)
# obj.db.desc = "obj description"
# exit = create.create_object("features.seethrough_exits.SeeThroughExitMixin", key="room", location=caller.location, destination=room)
# exit.db.desc = "exit description"
# exit.db.return_appearance_type = "destination_appearance"
# exit2 = create.create_object("features.delayed_exits.DelayedExitMixin", key="limbo", location=room, destination=caller.location)
# exit2.db.desc = "exit2 description"

# Testing See Through Exits
room = create.create_object("typeclasses.default_typeclasses.Room", key="room", location=None)
room.db.desc = "room description"
obj = create.create_object(key="obj", location=room)
obj.db.desc = "obj description"
exit = create.create_object("typeclasses.default_typeclasses.Exit", key="room", location=caller.location, destination=room)
exit.db.desc = "exit description"
exit.db.return_appearance_type = "destination_appearance"
exit2 = create.create_object("typeclasses.default_typeclasses.Exit", key="limbo", location=room, destination=caller.location)
exit2.db.desc = "exit2 description"
