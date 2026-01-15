from typing import List, Dict, Optional, Set
from .DSPDataLoader import load_tech_data, load_recipe_data

# Map recipe ID -> tech ID that unlocks it
tech_data = load_tech_data()
recipe_data = load_recipe_data()
recipe_to_tech = {}
for tech in tech_data:
    for recipe_id in tech.get("UnlockRecipes", []):
        recipe_to_tech[recipe_id] = tech["ID"]

# Map item_id -> recipe_ids that produce it
from collections import defaultdict
item_to_recipes = defaultdict(list)
for recipe in recipe_data:
    for result in recipe.get("Results", []):
        item_to_recipes[result].append(recipe["ID"])

techs_allowed_to_handcraft = {1001, 1002, 1201, 1401, 1601}
techs_needed_to_exit_handcrafting = {1001, 1002, 1201, 1401, 1601}
power_buildings = {2201, 2203}

items_needed_for_item = {
    1208: { 2208, 1501, 2311 }, # Critical Photon requires Ray Reciever, Solar Sail and EM-Rail Ejector
    1000: { 2306 }, # Water requires Water Pump
    1007: { 2307 }, # Raw Oil requires Oil Extractor
}

techs_needed_for_item = {
    1003: { 2901, 2902 }, # Silicon Ore requires interplanetary flight (TODO: Maybe make adjustable?)
    1004: { 2901, 2902 }, # Titanium Ore requires interplanetary flight (TODO: Maybe make adjustable?)
}

def get_required_techs_for_tech(tech_id: int, visited: Optional[Set[int]] = None) -> Set[int]:
    if visited is None:
        visited = set()
    if tech_id in visited:
        return set()

    visited.add(tech_id)

    tech = next((t for t in tech_data if t["ID"] == tech_id), None)
    if not tech:
        return set()

    required_techs = set()

    # Check for items that the tech needs, and recursively find matrix items from producers
    for item_id in tech.get("Items", []):
        # TODO: Currently this will always use the first recipe (which is hopefully the early game one)
        recipe_to_use = min(item_to_recipes.get(item_id, []))
        required_techs.add(recipe_to_tech[recipe_to_use])
        recipe = next((r for r in recipe_data if r["ID"] == recipe_to_use), None)
        # print(f"technology {tech["Name"]} requires item {item_id}, which requires recipe {recipe["Name"]}")
            
        for ingredient_id in recipe["Items"]:
            required_techs.update(get_required_techs_to_craft_item(ingredient_id, not tech_id in techs_allowed_to_handcraft))
        
            

    return required_techs

def get_required_techs_to_craft_item(item_id: int, include_recipes_for_machines = True, visited: Optional[Set[int]] = None) -> Set[int]:
    if visited is None:
        visited = set()
    if item_id in visited:
        return set()

    visited.add(item_id)
    
    required_techs = set()

    potential_recipes = item_to_recipes.get(item_id, [])

    if potential_recipes:
        # TODO: Currently this will always use the first recipe (which is hopefully the early game one)
        recipe_to_use = min(potential_recipes)
        # print(f"recipe {recipe_to_use} requires tech {recipe_to_tech[recipe_id]}")
        if recipe_to_tech.get(recipe_to_use):
            required_techs.add(recipe_to_tech[recipe_to_use])
        recipe = next((r for r in recipe_data if r["ID"] == recipe_to_use), None)

        machine_to_use = -1
        if recipe.get("PossibleMachines"):
            machine_to_use = min(recipe["PossibleMachines"])
        else:
            print(f"Missing Machine for recipe_id: {recipe_to_use}")

        # print(f"item {item_id} requires recipe {recipe["Name"]}, which requires machine {machine_to_use}")

        # TODO: Currently this will always use the first possible machine (which is hopefully the early game one)
        if include_recipes_for_machines:
            required_techs.update(get_required_techs_to_craft_item(machine_to_use, include_recipes_for_machines, visited))
            for power_building in power_buildings:
                required_techs.update(get_required_techs_to_craft_item(power_building, include_recipes_for_machines, visited))

        for ingredient_id in recipe["Items"]:
            # print(f"recipe {recipe["Name"]} requires item {ingredient_id}")
            required_techs.update(get_required_techs_to_craft_item(ingredient_id, include_recipes_for_machines, visited))
    else:
        # print(f"item_id {item_id} does not have a recipe")
        if items_needed_for_item.get(item_id):
            for needed_item in items_needed_for_item.get(item_id):
                required_techs.update(get_required_techs_to_craft_item(needed_item, include_recipes_for_machines, visited))

        if techs_needed_for_item.get(item_id):
            for needed_tech in techs_needed_for_item.get(item_id):
                required_techs.add(needed_tech)
        
    return required_techs