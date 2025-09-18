from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import DSPWorld

# This should ideally be a default setting that can be turned off
def has_basic_recipes(state, player):
    return (
        state.has("Basic Assembling", player)
        and state.has("Automatic Metallurgy", player)
        and state.has("Basic Logistics System", player)
        and state.has("Electromagnetic Matrix", player)
    )
def set_rules(dsp_world: "DSPWorld"):
    player = dsp_world.player
    multiworld = dsp_world.multiworld

    # Region rules
    set_rule(multiworld.get_entrance("Menu -> Game Start", player), lambda state: True)
    set_rule(multiworld.get_entrance("Game Start -> Electromagnetic Matrix", player), lambda state: has_basic_recipes(state, player))
    set_rule(multiworld.get_entrance("Electromagnetic Matrix -> Energy Matrix", player), lambda state: state.has("Energy Matrix", player))
    set_rule(multiworld.get_entrance("Energy Matrix -> Structure Matrix", player), lambda state: state.has("Structure Matrix", player))
    set_rule(multiworld.get_entrance("Structure Matrix -> Information Matrix", player), lambda state: state.has("Information Matrix", player))
    set_rule(multiworld.get_entrance("Information Matrix -> Gravity Matrix", player), lambda state: state.has("Gravity Matrix", player))
    set_rule(multiworld.get_entrance("Gravity Matrix -> Universe Matrix", player), lambda state: state.has("Universe Matrix", player))
    set_rule(multiworld.get_entrance("Universe Matrix -> Goal Complete", player), lambda state: state.has("Universe Matrix", player))