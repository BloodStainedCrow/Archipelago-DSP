from BaseClasses import Region
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DSPWorld
    
    
def create_region(name, player, multiworld):
    region = Region(name, player, multiworld)
    multiworld.regions.append(region)
    return region

def create_regions(dsp_world: "DSPWorld"):
    player = dsp_world.player
    multiworld = dsp_world.multiworld
    
    # Create regions
    menu = create_region("Menu", player, multiworld)
    game_start = create_region("Game Start", player, multiworld)
    tier1_matrix = create_region("Electromagnetic Matrix", player, multiworld)
    tier2_matrix = create_region("Energy Matrix", player, multiworld)
    tier3_matrix = create_region("Structure Matrix", player, multiworld)
    tier4_matrix = create_region("Information Matrix", player, multiworld)
    tier5_matrix = create_region("Gravity Matrix", player, multiworld)
    tier6_matrix = create_region("Universe Matrix", player, multiworld)
    goal_complete = create_region("Goal Complete", player, multiworld)
    
    # Create connections
    menu.add_exits(["Game Start"])
    game_start.add_exits(["Electromagnetic Matrix"])
    tier1_matrix.add_exits(["Energy Matrix"])
    tier2_matrix.add_exits(["Structure Matrix"])
    tier3_matrix.add_exits(["Information Matrix"])
    tier4_matrix.add_exits(["Gravity Matrix"])
    tier5_matrix.add_exits(["Universe Matrix"])
    tier6_matrix.add_exits(["Goal Complete"])
