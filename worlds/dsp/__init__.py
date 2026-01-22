from worlds.AutoWorld import WebWorld, World
from BaseClasses import Location, Item, Tutorial, MultiWorld, LocationProgressType
from . import Items, Locations, Regions, Rules
from .DSPDataLoader import load_tech_data
tech_data = load_tech_data()

class DSPItem(Item):
    game: str = "Dyson Sphere Program"

class DSPLocation(Location):
    game: str = "Dyson Sphere Program"
    
class DSPWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Dyson Sphere Program randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Prototy"]
    )]
    theme = "dirt"

class DSPWorld(World):
    """
    Dyson Sphere Program is a sci-fi strategy game where you build and manage a factory in space.
    """
    game = 'Dyson Sphere Program'
    web = DSPWeb()

    options_dataclass = Options.DSPOptions
    options: Options.DSPOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).
    
    item_name_to_id = {item[0]: item[1] for item in Items.get_potential_item_set()}
    location_name_to_id = {loc[0]: loc[1] for loc in Locations.possible_location_set()}
    
    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        
    def create_regions(self):
        Regions.create_regions(self)
        Locations.create_locs(self.options.exclude_upgrade_locs, self.options.max_matrix_needed)
        
        # Add locations into regions
        for region in self.multiworld.get_regions(self.player):
            for loc in [location for location in Locations.locations if location.region == region.name]:
                location = DSPLocation(player=self.player, name=loc.name, address=loc.id, parent=region)
                location.progress_type = loc.progress_type
                region.locations.append(location)
    
    def create_item(self, name: str) -> DSPItem:
        Items.create_items(goal_tech_id, goal_tech, self.options.progressive)
        item: Items.ItemDef = next((item for item in Items.items if item.name == name), None)
        return DSPItem(name, item.classification, item.id, self.player)
    
    def set_rules(self):
        Rules.set_rules(self)
        goal_tech = next((t["Name"] for t in tech_data if t.get("Name") == self.options.goal_tech), None)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("[GOAL] " + goal_tech, self.player)
    
    def create_items(self) -> None:
        goal_tech_id = next((t["ID"] for t in tech_data if t.get("Name") == self.options.goal_tech), None)
        goal_tech = next((t["Name"] for t in tech_data if t.get("ID") == goal_tech_id), None)
        Items.create_items(goal_tech_id, goal_tech, self.options.progressive)
        for item in Items.items:
            prefill_loc = None
            if item.prefill_location:
                prefill_loc = self.get_location(item.prefill_location)
                prefill_loc.place_locked_item(DSPItem(item.name, item.classification, item.id, self.player))
            else:
                for _ in range(item.count):
                    self.multiworld.itempool.append(DSPItem(item.name, item.classification, item.id, self.player))
    