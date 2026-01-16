from typing import Optional
from .DSPDataLoader import load_tech_data
from .Options import FIRST_UPGRADE_ID
tech_data = load_tech_data()

# This returns a unique name for each technology, deterministically
def item_name_from_tech_name(tech_id: int, tech_name: str) -> str:
    repeat_id = get_repeat_id(tech_id, tech_name)
    if repeat_id == None:
        # No duplicated names to fix up
        return f"{tech_name}"
    else:
        return f"{tech_name} {repeat_id + 1}"


# This returns a unique name for each technology, deterministically
def location_name_from_tech_name(tech_id: int, tech_name: str) -> str:
    repeat_id = get_repeat_id(tech_id, tech_name)
    if repeat_id == None:
        # No duplicated names to fix up
        return f"{tech_name} Research"
    else:
        return f"{tech_name} Research {repeat_id + 1}"


def get_repeat_id(tech_id: int, tech_name: str) -> Optional[int]:
    techs_with_this_name = [tech["ID"] for tech in tech_data if tech["Name"] == tech_name]
    if len(techs_with_this_name) == 1:
        return None
    else:
        return techs_with_this_name.index(tech_id)

def get_progressive_tech_name(tech_id: int, tech_name: str) -> Optional[str]:
    if tech_id >= FIRST_UPGRADE_ID:
        return f"Progressive {tech_name}"
    else:
        return None

def get_item_name_with_progressive(tech_id: int, tech_name: str) -> str:
    if tech_id >= FIRST_UPGRADE_ID:
        return f"Progressive {tech_name}"
    else:
        return item_name_from_tech_name(tech_id, tech_name)