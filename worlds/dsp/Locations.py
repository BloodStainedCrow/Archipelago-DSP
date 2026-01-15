from BaseClasses import LocationProgressType
from typing import List, Dict, Optional, Set
from .DSPDataLoader import load_tech_data
from .Requirements import techs_allowed_to_handcraft, get_required_techs_for_tech
from .Naming import location_name_from_tech_name
from .Options import FIRST_UPGRADE_ID, EXCLUDE_UPGRADE_LOCS, MAX_MATRIX_NEEDED

class LocationDef:
    def __init__(self,
                 id: Optional[int],
                 name: str,
                 region: str,
                 progress_type: LocationProgressType = LocationProgressType.DEFAULT):
        self.type = type
        self.id = id
        self.name = name
        self.region = region
        self.progress_type = progress_type

# Matrix item ID -> Region name mapping
MATRIX_ITEMS = {
    6001: "Electromagnetic Matrix",
    6002: "Energy Matrix",
    6003: "Structure Matrix",
    6004: "Information Matrix",
    6005: "Gravity Matrix",
    6006: "Universe Matrix",
}
MATRIX_ITEM_IDS = set(MATRIX_ITEMS.keys())

# Map recipe ID -> tech ID that unlocks it
tech_data = load_tech_data()

# Should be region (matrix type) -> set of location names
location_name_groups: Dict[str, Set[str]] = {}

def get_matrix_items_for_tech(tech) -> Set[int]:
    matrix_items = set(i for i in tech.get("Items", []) if i in MATRIX_ITEM_IDS)

    return matrix_items

# Build the locations list
locations: List[LocationDef] = []

max_matrix_id_allowed = list(MATRIX_ITEMS.keys())[list(MATRIX_ITEMS.values()).index(MAX_MATRIX_NEEDED)]

for tech in tech_data:
    if tech.get("IsHiddenTech"):
        continue  # Skip hidden techs
    
    tech_id = tech.get("ID")
    if tech_id == 1:
        continue # Skip the initial tech

    tech_name = tech.get("Name")

    # Gather all matrix items directly required
    all_matrix_items = get_matrix_items_for_tech(tech)

    progress_type = LocationProgressType.EXCLUDED if tech_id >= FIRST_UPGRADE_ID and EXCLUDE_UPGRADE_LOCS else LocationProgressType.DEFAULT

    if all_matrix_items:
        highest_matrix_id = max(all_matrix_items)
        region = MATRIX_ITEMS.get(highest_matrix_id, "Game Start")

        # FIXME: This might fail if a tech does not need a matrix but a prereq does.
        if highest_matrix_id > max_matrix_id_allowed:
            progress_type = LocationProgressType.EXCLUDED

        if tech_id in techs_allowed_to_handcraft:
            region = "Game Start"
    else:
        region = "Game Start"

    location_name = location_name_from_tech_name(tech_id, tech_name)

    location = LocationDef(
        id=tech_id,
        name=location_name,
        region=region,
        progress_type=progress_type
    )

    # Group location names by region
    if region not in location_name_groups:
        location_name_groups[region] = set()
    location_name_groups[region].add(location_name)

    locations.append(location)