"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia.objects.objects import DefaultExit
from features.exit_delay import DelayedExitMixin

class Exit(DelayedExitMixin, DefaultExit):

    pass
