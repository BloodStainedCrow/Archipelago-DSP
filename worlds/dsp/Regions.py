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
    electromagnetic_matrix = create_region("Electromagnetic Matrix", player, multiworld)
    energy_matrix = create_region("Energy Matrix", player, multiworld)
    structure_matrix = create_region("Structure Matrix", player, multiworld)
    information_matrix = create_region("Information Matrix", player, multiworld)
    gravity_matrix = create_region("Gravity Matrix", player, multiworld)
    universe_matrix = create_region("Universe Matrix", player, multiworld)
    goal_complete = create_region("Goal Complete", player, multiworld)
    
    # Create connections
    menu.add_exits(["Game Start"])
    game_start.add_exits(["Electromagnetic Matrix"])
    electromagnetic_matrix.add_exits(["Energy Matrix"])
    energy_matrix.add_exits(["Structure Matrix"])
    structure_matrix.add_exits(["Information Matrix"])
    information_matrix.add_exits(["Gravity Matrix"])
    gravity_matrix.add_exits(["Universe Matrix"])
    universe_matrix.add_exits(["Goal Complete"])
