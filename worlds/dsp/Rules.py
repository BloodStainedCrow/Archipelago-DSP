from typing import TYPE_CHECKING, Iterable, Set, Mapping
from worlds.generic.Rules import set_rule
from .Requirements import get_required_techs_to_craft_item, techs_allowed_to_handcraft, techs_needed_to_exit_handcrafting
from .DSPDataLoader import load_tech_data, load_recipe_data
from .Naming import item_name_from_tech_name, location_name_from_tech_name, get_item_name_with_progressive

if TYPE_CHECKING:
    from . import DSPWorld

tech_data = load_tech_data()
recipe_data = load_recipe_data()

def get_requires_technologies_to_research_with(sciences: Iterable[str], use_prog: bool) -> Set[tuple[str, int]]:
    techs = set()
    for science in sciences:
        # We need to be able to create the sciences
        # Get item_id
        # FIXME: For now (since I only care about the matrices where this holds, I just search for the recipe with this name and use the output)
        recipe = next((r for r in recipe_data if r["Name"] == science), None)
        item_id = recipe["Results"][0]

        technologies = get_required_techs_to_craft_item(item_id)

        if use_prog:
            item_name_list = list(map(lambda tech_id: get_item_name_with_progressive(tech_id, next((t for t in tech_data if t["ID"] == tech_id), None)["Name"]), technologies))
        else:
            item_name_list = list(map(lambda tech_id: item_name_from_tech_name(tech_id, next((t for t in tech_data if t["ID"] == tech_id), None)["Name"]), technologies))

        techs.update(map(lambda tech_name: tuple([tech_name, len(list((t for t in item_name_list if t == tech_name)))]), item_name_list))

    return techs

def get_requires_technologies_to_research_with_item_ids(sciences: Iterable[int], allow_handcraft: bool, use_prog: bool) -> Set[tuple[str, int]]:
    techs = set()
    for item_id in sciences:
        # We need to be able to create the sciences
        technologies = get_required_techs_to_craft_item(item_id, not allow_handcraft)

        item_name_list = None 

        if use_prog:
            item_name_list = list(map(lambda tech_id: get_item_name_with_progressive(tech_id, next((t for t in tech_data if t["ID"] == tech_id), None)["Name"]), technologies))
        else:
            item_name_list = list(map(lambda tech_id: item_name_from_tech_name(tech_id, next((t for t in tech_data if t["ID"] == tech_id), None)["Name"]), technologies))


        techs.update(map(lambda tech_name: tuple([tech_name, len(list((t for t in item_name_list if t == tech_name)))]), item_name_list))

    return techs

def mapping_from_set(input_set: Set[tuple[str, int]]) -> Mapping[str, int]:
    mapping = {}
    for research in input_set:
        tech_name = research[0]
        tech_count = research[1]
        mapping[tech_name] = tech_count
    return mapping

def set_rules(dsp_world):
    player = dsp_world.player
    multiworld = dsp_world.multiworld

    use_prog = dsp_world.options.progressive == True

    # Region rules
    set_rule(multiworld.get_entrance("Menu -> Game Start", player), lambda state: True)
    set_rule(multiworld.get_entrance("Game Start -> Electromagnetic Matrix", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Electromagnetic Matrix"], use_prog)), player))
    set_rule(multiworld.get_entrance("Electromagnetic Matrix -> Energy Matrix", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Electromagnetic Matrix", "Energy Matrix"], use_prog)), player))
    set_rule(multiworld.get_entrance("Energy Matrix -> Structure Matrix", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Electromagnetic Matrix", "Energy Matrix", "Structure Matrix"], use_prog)), player))
    set_rule(multiworld.get_entrance("Structure Matrix -> Information Matrix", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Electromagnetic Matrix", "Energy Matrix", "Structure Matrix", "Information Matrix"], use_prog)), player))
    set_rule(multiworld.get_entrance("Information Matrix -> Gravity Matrix", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Electromagnetic Matrix", "Energy Matrix", "Structure Matrix", "Information Matrix", "Gravity Matrix"], use_prog)), player))
    set_rule(multiworld.get_entrance("Gravity Matrix -> Universe Matrix", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Universe Matrix"], use_prog)), player))
    set_rule(multiworld.get_entrance("Universe Matrix -> Goal Complete", player), lambda state: state.has_all_counts(mapping_from_set(get_requires_technologies_to_research_with(["Universe Matrix"], use_prog)), player))

    # Ensure being able to craft
    for tech_id in techs_needed_to_exit_handcrafting:
        tech = next((t for t in tech_data if t["ID"] == tech_id), None)
        tech_name = tech["Name"]

        item_name = item_name_from_tech_name(tech_id, tech_name)
        multiworld.local_early_items[player][item_name] = 1


    # Location Rules
    for tech in tech_data:
        if tech.get("IsHiddenTech"):
            continue  # Skip hidden techs
        
        tech_id = tech.get("ID")
        if tech_id == 1:
            continue # Skip the initial tech

        tech_name = tech["Name"]
        location_name = location_name_from_tech_name(tech_id, tech_name)

        researches_needed = set(get_requires_technologies_to_research_with_item_ids(tech["Items"], tech_id in techs_allowed_to_handcraft, use_prog))
        mapping = mapping_from_set(researches_needed)
        # print(mapping)
        # if len(researches_needed) > 0:
        # FIXME: Ensure that all prereq locations are researchable
        set_rule(multiworld.get_location(location_name, player), lambda state, mapping=mapping: state.has_all_counts(mapping, player))