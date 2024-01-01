"""
See-through Exit
This is a mixin that allows an Exit to return it's destinations description 
when subject to a look command.

INSTALLATION:
1. Have Exit typeclass inherit from SeeThroughExitMixin()
    from features.exit_seethrough import SeeThroughExitMixin
    class Exit(SeeThroughExitMixin, DefaultExit):
        pass
"""
from evennia import DefaultExit


class SeeThroughExitMixin(DefaultExit):
    """
    This is a mixin that allows an Exit to return it's destinations description 
    when subject to a look command.
    """

    def return_appearance(self, looker):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        
        Attributes:
            return_appearance_type: (String) dictates the description returned.
                "exit_desc" - will use the description of the exit object (default).
                "destination_desc" - will use the description of the destination object only - no content lists.
                "destination_appearance" - will use the full appearance of the destination object - incl contents.
                "preamble" - The string displayed before the destination's appearance.
            
        Args:
            looker (Object): Object doing the looking.
        """
        if not looker:
            return ""
        
        if not self.destination:
            return super().return_appearance(looker)
        
        return_appearance_type = self.attributes.get("return_appearance_type", default = "exit_desc")        
        match return_appearance_type:
            case "exit_desc":
                return super().return_appearance(looker)
            case "destination_desc":
                string = ""
                string += self.attributes.get("preamble", default = "Looking in this direction you see: ")
                string += f"|c{self.get_display_name(looker, pose=True)}|n\n"
                string += f"{self.destination.db.desc}"
                return string
            case "destination_appearance":
                string = ""
                string += self.attributes.get("preamble", default = "Looking in this direction you see: ")
                string += f"|c{self.get_display_name(looker, pose=True)}|n\n"
                string += f"{looker.at_look(destination)}"
                return string
        