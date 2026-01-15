from BaseClasses import ItemClassification
from typing import List, Optional
from .DSPDataLoader import load_tech_data
from .Requirements import get_required_techs_for_tech
from .Naming import item_name_from_tech_name, location_name_from_tech_name
import re

from .Options import GOAL_TECH_ID, FIRST_UPGRADE_ID, GOAL_TECH

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

# Progressive items grouped by their base name
progressive_items_by_group = {}

needed_techs_for_victory = get_required_techs_for_tech(GOAL_TECH_ID)

for tech in tech_data:
    if tech.get("IsHiddenTech"):
        continue  # Skip hidden tech

    tech_id = tech.get("ID")
    if tech_id == 1:
        continue # Skip the initial tech

    tech_name = tech.get("Name")
    unlock_recipes = set(tech.get("UnlockRecipes", []))

    classification = (
        ItemClassification.progression
        if (tech_id in needed_techs_for_victory)
        else ItemClassification.filler
    )

    item_name = item_name_from_tech_name(tech_id, tech_name)
    # FIXME: Readd progressives
    
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
    id=GOAL_TECH_ID,
    name=GOAL_TECH,
    classification=ItemClassification.progression,
    count=1,
    prefill_location=location_name_from_tech_name(GOAL_TECH_ID, GOAL_TECH),
    progressive_group=None
)
items.append(goal_item)