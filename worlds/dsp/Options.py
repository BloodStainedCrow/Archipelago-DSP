from dataclasses import dataclass

from Options import Visibility, Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, FreeText

# Constants for Options
FIRST_UPGRADE_ID = 2000
GOAL_ITEM_OFFSET = 12000 * 2
PROGRESSIVE_ITEM_OFFSET = 12000


# Options
EXCLUDE_UPGRADE_LOCS = True

class GoalTech(FreeText):
    """
    The Technology needed to unlock to win. Needs to be obtainable without using matrices past the "Highest Matrix needed" (This will be verified properly in the future).
    Unfortunately not all technologies currently work, if the game fails to generate citing "Game appears unbeatable" maybe try a different goal technology.
    """

    display_name = "Goal Tech"

    default = "Mission Completed!"

class ExcludeUpgradeLocs(Toggle):
    """
    Exclude Upgrades from having progression items.
    """

    display_name = "Exclude Upgrade Locs"
    default = True

class MaxMatrixNeeded(Choice):
    """
    Highest Matrix needed to win.
    All technologies requiring more advanced matricies than this will be excluded from holding progression items.
    """

    display_name = "Highest Matrix needed"
    
    option_blue = 6001
    option_red = 6002
    option_yellow = 6003
    option_purple = 6004
    option_green = 6005
    option_white = 6006
    
    default = option_green

class UseProgressive(Toggle):
    """
    Make Upgrades progressive. Turning this off is experimental and *could* make the game impossible to beat.
    """

    visibility = Visibility.template | Visibility.complex_ui

    display_name = "Progressive Upgrade"
    
    default = True

@dataclass
class DSPOptions(PerGameCommonOptions):
    goal_tech: GoalTech
    exclude_upgrade_locs: ExcludeUpgradeLocs
    max_matrix_needed: MaxMatrixNeeded
    progressive: UseProgressive