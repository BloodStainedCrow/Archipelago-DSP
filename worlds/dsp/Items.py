from BaseClasses import ItemClassification
from typing import List, Optional
from .DSPDataLoader import load_tech_data
from .Requirements import get_required_techs_for_tech
from .Naming import item_name_from_tech_name, location_name_from_tech_name, get_progressive_tech_name, get_item_name_with_progressive
import re

from .Options import FIRST_UPGRADE_ID, GOAL_ITEM_OFFSET, PROGRESSIVE_ITEM_OFFSET

class ItemDef:
    def __init__(self,
                 id: Optional[int],
                 name: str,
                 classification: ItemClassification,
                 count: int,
                 prefill_location: Optional[str] = None,
                 progressive_group: Optional[str] = None):
        self.type = type
        self.id = id
        self.name = name
        self.classification = classification
        self.count = count
        self.prefill_location = prefill_location
        self.progressive_group = progressive_group

# Load tech data
tech_data = load_tech_data()

# Build items
items: List[ItemDef] = []

def get_progressive_tech_id(tech_id: int, tech_name: str) -> Optional[int]:
        techs_with_this_name = [tech["ID"] for tech in tech_data if tech["Name"] == tech_name]
        if len(techs_with_this_name) == 1:
            return None
        else:
            # TODO: This assumes that upgrades will always increase the ids
            return min(techs_with_this_name) + PROGRESSIVE_ITEM_OFFSET

def create_items(goal_tech_id: int, goal_tech: str, use_progressive: bool):
    # FIXME: This needs to take in account the required items for all prereqs!
    needed_techs_for_victory = get_required_techs_for_tech(goal_tech_id)

    for tech in tech_data:
        if tech.get("IsHiddenTech"):
            continue  # Skip hidden tech

        tech_id = tech.get("ID")
        if tech_id == 1:
            continue # Skip the initial tech

        if tech_id == goal_tech_id:
            continue # Skip the goal tech

        tech_name = tech.get("Name")
        unlock_recipes = set(tech.get("UnlockRecipes", []))

        classification = (
            ItemClassification.progression
            if (tech_id in needed_techs_for_victory)
            else ItemClassification.filler
        )

        item_name = None

        if use_progressive:
            item_name = get_item_name_with_progressive(tech_id, tech_name)
            prog_tech_id = get_progressive_tech_id(tech_id, tech_name)
            if prog_tech_id:
                tech_id = prog_tech_id
        else:
            item_name = item_name_from_tech_name(tech_id, tech_name)
        
        # print(item_name + ": " + str(classification))
        item = ItemDef(
            id=tech_id,
            name=item_name,
            classification=classification,
            count=1,
            prefill_location=None,
            progressive_group=None
        )

        items.append(item)

    # Add completion item
    goal_item = ItemDef(
        id=goal_tech_id + GOAL_ITEM_OFFSET,
        name=goal_tech,
        classification=ItemClassification.progression,
        count=1,
        prefill_location=location_name_from_tech_name(goal_tech_id, goal_tech),
        progressive_group=None
    )
    items.append(goal_item)