from BaseClasses import LocationProgressType
from typing import List, Dict, Optional, Set
from .DSPItemTypeEnum import DSPType
from .DSPDataLoader import load_tech_data, load_recipe_data, ensure_unique_name

class LocationDef:
    def __init__(self,
                 type: Optional[DSPType],
                 id: Optional[int],
                 name: str,
                 region: str,
                 progress_type: LocationProgressType = LocationProgressType.DEFAULT):
        self.type = type
        self.id = id
        self.name = name
        self.region = region
        self.progress_type = progress_type

# Any tech ID >= this is considered an "upgrade" tech
FIRST_UPGRADE_ID = 2000

# Matrix item ID -> Region name mapping
MATRIX_REQUIREMENTS = {
    6001: 'Electromagnetic Matrix',
    6002: 'Energy Matrix',
    6003: 'Structure Matrix',
    6004: 'Information Matrix',
    6005: 'Gravity Matrix',
    6006: 'Universe Matrix'
}
MATRIX_ITEM_IDS = set(MATRIX_REQUIREMENTS.keys())

# Items that don't need a recipe (gathered from world)
NON_RECIPE_ITEM_IDS = {1006, 1030}

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

# location_name_groups: ClassVar[Dict[str, Set[str]]] = {}
# Should be region (matrix type) -> set of location names
location_name_groups: Dict[str, Set[str]] = {}

# Helper: Get matrix items required by a given tech
def get_matrix_items_for_tech(tech_id: int, visited: Optional[Set[int]] = None) -> Set[int]:
    if visited is None:
        visited = set()
    if tech_id in visited:
        return set()

    visited.add(tech_id)

    tech = next((t for t in tech_data if t["ID"] == tech_id), None)
    if not tech:
        return set()

    matrix_items = set(i for i in tech.get("Items", []) if i in MATRIX_ITEM_IDS)

    # Check for items that the tech needs, and recursively find matrix items from producers
    for item in tech.get("Items", []):
        if item in MATRIX_ITEM_IDS or item in NON_RECIPE_ITEM_IDS:
            continue

        for recipe_id in item_to_recipes.get(item, []):
            unlocking_tech = recipe_to_tech.get(recipe_id)
            if unlocking_tech:
                matrix_items.update(get_matrix_items_for_tech(unlocking_tech, visited))

    return matrix_items

# Build the locations list
locations: List[LocationDef] = []

# Special location
locations.append(LocationDef(None, None, 'Mission Completed!', 'Universe Matrix'))

used_location_names = {}

for tech in tech_data:
    if tech.get("IsHiddenTech"):
        continue  # Skip hidden techs
    
    tech_id = tech.get("ID")
    if tech_id == 1:
        continue # Skip the initial tech

    tech_name = tech.get("Name")

    # Gather all matrix items directly or indirectly required
    all_matrix_items = get_matrix_items_for_tech(tech_id)

    if all_matrix_items:
        highest_matrix_id = max(all_matrix_items)
        region = MATRIX_REQUIREMENTS.get(highest_matrix_id, "Game Start")
    else:
        region = "Game Start"

    base_location_name = f"{tech_name} Research"
    unique_location_name = ensure_unique_name(base_location_name, used_location_names)

    location = LocationDef(
        type=DSPType.ITEM,
        id=tech_id,
        name=unique_location_name,
        region=region,
        progress_type = LocationProgressType.EXCLUDED if tech_id >= FIRST_UPGRADE_ID else LocationProgressType.DEFAULT
    )

    # Group location names by region
    if region not in location_name_groups:
        location_name_groups[region] = set()
    location_name_groups[region].add(unique_location_name)

    locations.append(location)