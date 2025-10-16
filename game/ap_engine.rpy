init python:
    import os
    import json

    if "localappdata" in os.environ:
        CONNECTIONS_PATH = os.path.expandvars(r"%localappdata%/APPF2e")
    else:
        CONNECTIONS_PATH = os.path.expandvars(r"$HOME/APPF2e")
    if not os.path.exists(CONNECTIONS_PATH):
        os.makedirs(CONNECTIONS_PATH)

    def game_watcher():

        send_locations(store.checked)
        get_items()
    
    def send_locations(locations):

        for location in locations:
            with open(os.path.join(CONNECTIONS_PATH, "send" + str(LOCATION_NAME_TO_ID[location])), 'w') as f:
                f.close()
    
    def get_items():

        new_items = []

        for root, dirs, files in os.walk(CONNECTIONS_PATH):
            for f in files:
                if f.startswith("AP"):
                    if f not in store.collected:
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            new_items.append(int(current.readline()))
                            current.close()
                        store.collected.append(f)
        if new_items:
            renpy.call("receive_items", new_items, from_current=True)
    
    def read_files():

        found_files = 0

        for root, dirs, files in os.walk(CONNECTIONS_PATH):
            for f in files:
                if f.endswith(".cfg"):
                    
                    if f.startswith("strict_logic"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.strict_logic = True
                            current.close()
                        found_files += 1
                    
                    if f.startswith("use_abp"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.use_abp = True
                            current.close()
                        found_files += 1

                    if f.startswith("include_exploration_activities"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            if current.readline() == "1":
                                store.include_exploration_activities = True
                            current.close()
                        found_files += 1
                    
                    if "Room" in f:
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.rooms[f.split(".")[0].replace("_", " ")] = json.loads(current.readline())
                            current.close()
                        found_files += 1
                    
                    if f.startswith("Ancestries"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.starting["Ancestries"] = current.readline()
                            current.close()
                        found_files += 1

                    if f.startswith("Backgrounds"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.starting["Backgrounds"] = current.readline()
                            current.close()
                        found_files += 1
                    
                    if f.startswith("Classes"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.starting["Classes"] = current.readline()
                            current.close()
                        found_files += 1
                    
                    if f.startswith("Weapons"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.starting["Weapons"] = current.readline()
                            current.close()
                        found_files += 1

                    if f.startswith("Armors"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.starting["Armors"] = current.readline()
                            current.close()
                        found_files += 1

                    if f.startswith("Shields"):
                        with open(os.path.join(CONNECTIONS_PATH, f), 'r') as current:
                            store.starting["Shields"] = current.readline()
                            current.close()
                        found_files += 1
        
        # Not enough files were found, so there's something gone wrong
        if found_files < 10:
            renpy.call("file_error")
    
    def requirements_by_level(level: int) -> bool:
        # Returns True if the player meets the requirements for the given level

        requirements = {
            "Level Up" : 0,
            "Progressive Weapon Rune" : 0,
            "Progressive Armor Rune" : 0,
            "Apex Items Token" : 0
        }

        if level >= 2:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Weapon Rune"] += 1
        if level >= 3:
            requirements["Level Up"] += 1
        if level >= 4:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Weapon Rune"] += 1
        if level >= 5:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Armor Rune"] += 1
        if level >= 6:
            requirements["Level Up"] += 1
        if level >= 7:
            requirements["Level Up"] += 1
        if level >= 8:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Armor Rune"] += 1
        if level >= 9:
            requirements["Level Up"] += 1
        if level >= 10:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Weapon Rune"] += 1
        if level >= 11:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Armor Rune"] += 1
        if level >= 12:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Weapon Rune"] += 1
        if level >= 13:
            requirements["Level Up"] += 1
        if level >= 14:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Armor Rune"] += 1
        if level >= 15:
            requirements["Level Up"] += 1
        if level >= 16:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Weapon Rune"] += 1
        if level >= 17:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Apex Items Token"] += 1
        if level >= 18:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Armor Rune"] += 1
        if level >= 19:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Weapon Rune"] += 1
        if level >= 20:
            requirements["Level Up"] += 1
            if not store.use_abp: requirements["Progressive Armor Rune"] += 1

        for requirement in requirements:
            if store.inventory[requirement] < requirements[requirement]:
                return False
        
        return True

    def use_token(token):
        if token in store.inventory:
            store.inventory[token] -= 1

# This is the list of locations that have been checked by the player listed by their names
default checked = []
# This is the dictionary of in-game items possessed listed by their names and pointing to their quantities
default inventory = {
    "Level Up": 0,
    "Progressive Weapon Rune" : 0,
    "Progressive Armor Rune" : 0,
    "Progressive Shield Rune" : 0,
    "Apex Items Token" : 0
}
# This is the list of Archipelago Items that have been received by their filenames
default collected = []
# This should be True once the victory condition has been met
default victory_achieved = False
# This should be true if we want to receive items without displaying any messages
default receive_silently = True
# This determines if the Strict Logic option is on and the player can only fight enemies that they are appropriately leveled for
default strict_logic = False
# This determines if the Use ABP option is on and the player doesn't need to track weapon and armor runes or apex items
default use_abp = False
# This determines if the Include Exploration Activities option is on
default include_exploration_activities = False
default starting = {
    "Ancestries" : "",
    "Backgrounds" : "",
    "Classes" : "",
    "Weapons" : "",
    "Armors" : "",
    "Shields" : ""
}
# This stores all of the data for the rooms in the game
default rooms = {
    "Room 1" : {
            "Level": 1,
            "Difficulty": "",
            "Creatures": [],
            "Doors": [],
            "Keys": []
    }
}
# These are the lookup tables for converting between IDs and English names of items and locations
define ITEM_NAME_TO_ID = {
    "Level Up" : 1,
    "Progressive Weapon Rune" : 2,
    "Progressive Armor Rune" : 3,
    "Apex Items Token" : 4,
    "Rest Token" : 5,
    "Ancestry Feat Token" : 6,
    "General Feat Token" : 7,
    "Skill Training Token" : 8,
    "Weapon Token" : 9,
    "Armor Token" : 10,
    "Shield Token" : 11,
    "Wand Token" : 12,
    "Staff Token" : 13,
    "Magic Item Token" : 14,
    "Consumable Token" : 15,
    "Apex Item Token" : 16,
    "Property Rune Token" : 17,
    "Material Token" : 18,
    "Healing Potion Token" : 19,
    "Elixir of Life Token" : 20,
    "Progressive Shield Rune" : 21,
    "Hero Point" : 22,
    "Avoid Notice Unlock" : 23,
    "Defend Unlock" : 24,
    "Detect Magic Unlock" : 25,
    "Repeat a Spell Unlock" : 26,
    "Scout Unlock" : 27,
    "Search Unlock" : 28,
    "Sustain an Effect Unlock" : 29,
    "Cover Tracks Unlock" : 30,
    "Hustle Unlock" : 31,
    "Investigate Unlock" : 32,
    "Track Unlock" : 33,
    "Red Key" : 101,
    "Blue Key" : 102,
    "Green Key" : 103,
    "Yellow Key" : 104,
    "Cyan Key" : 105,
    "Magenta Key" : 106,
    "White Key" : 107,
    "Black Key" : 108,
    "Gray Key" : 109,
    "Orange Key" : 110,
    "Azure Key" : 111,
    "Chartreuse Key" : 112,
    "Teal Key" : 113,
    "Violet Key" : 114,
    "Pink Key" : 115,
    "Amber Key" : 116,
    "Indigo Key" : 117,
    "Purple Key" : 118,
    "Crimson Key" : 119,
    "Vermilion Key" : 120
}
define ID_TO_ITEM_NAME = {v: k for k, v in ITEM_NAME_TO_ID.items()}
define LOCATION_NAME_TO_ID = {
    "Room 1 A" : 11,
    "Room 1 B" : 12,
    "Room 1 C" : 13,
    "Room 1 D" : 14,
    "Room 1 E" : 15,
    "Room 2 A" : 21,
    "Room 2 B" : 22,
    "Room 2 C" : 23,
    "Room 2 D" : 24,
    "Room 2 E" : 25,
    "Room 3 A" : 31,
    "Room 3 B" : 32,
    "Room 3 C" : 33,
    "Room 3 D" : 34,
    "Room 3 E" : 35,
    "Room 4 A" : 41,
    "Room 4 B" : 42,
    "Room 4 C" : 43,
    "Room 4 D" : 44,
    "Room 4 E" : 45,
    "Room 5 A" : 51,
    "Room 5 B" : 52,
    "Room 5 C" : 53,
    "Room 5 D" : 54,
    "Room 5 E" : 55,
    "Room 6 A" : 61,
    "Room 6 B" : 62,
    "Room 6 C" : 63,
    "Room 6 D" : 64,
    "Room 6 E" : 65,
    "Room 7 A" : 71,
    "Room 7 B" : 72,
    "Room 7 C" : 73,
    "Room 7 D" : 74,
    "Room 7 E" : 75,
    "Room 8 A" : 81,
    "Room 8 B" : 82,
    "Room 8 C" : 83,
    "Room 8 D" : 84,
    "Room 8 E" : 85,
    "Room 9 A" : 91,
    "Room 9 B" : 92,
    "Room 9 C" : 93,
    "Room 9 D" : 94,
    "Room 9 E" : 95,
    "Room 10 A" : 101,
    "Room 10 B" : 102,
    "Room 10 C" : 103,
    "Room 10 D" : 104,
    "Room 10 E" : 105,
    "Room 11 A" : 111,
    "Room 11 B" : 112,
    "Room 11 C" : 113,
    "Room 11 D" : 114,
    "Room 11 E" : 115,
    "Room 12 A" : 121,
    "Room 12 B" : 122,
    "Room 12 C" : 123,
    "Room 12 D" : 124,
    "Room 12 E" : 125,
    "Room 13 A" : 131,
    "Room 13 B" : 132,
    "Room 13 C" : 133,
    "Room 13 D" : 134,
    "Room 13 E" : 135,
    "Room 14 A" : 141,
    "Room 14 B" : 142,
    "Room 14 C" : 143,
    "Room 14 D" : 144,
    "Room 14 E" : 145,
    "Room 15 A" : 151,
    "Room 15 B" : 152,
    "Room 15 C" : 153,
    "Room 15 D" : 154,
    "Room 15 E" : 155,
    "Room 16 A" : 161,
    "Room 16 B" : 162,
    "Room 16 C" : 163,
    "Room 16 D" : 164,
    "Room 16 E" : 165,
    "Room 17 A" : 171,
    "Room 17 B" : 172,
    "Room 17 C" : 173,
    "Room 17 D" : 174,
    "Room 17 E" : 175,
    "Room 18 A" : 181,
    "Room 18 B" : 182,
    "Room 18 C" : 183,
    "Room 18 D" : 184,
    "Room 18 E" : 185,
    "Room 19 A" : 191,
    "Room 19 B" : 192,
    "Room 19 C" : 193,
    "Room 19 D" : 194,
    "Room 19 E" : 195,
    "Room 20 A" : 201,
    "Room 20 B" : 202,
    "Room 20 C" : 203,
    "Room 20 D" : 204,
    "Room 20 E" : 205,
    "Boss Room A" : 10001,
    "Boss Room B" : 10002,
    "Boss Room C" : 10003,
    "Boss Room D" : 10004,
    "Boss Room E" : 10005,
    "Boss Room F" : 10006,
    "Boss Room G" : 10007,
    "Boss Room H" : 10008,
    "Boss Room I" : 10009,
    "Boss Room J" : 10010,
    "Boss Room K" : 10011,
    "Boss Room L" : 10012,
    "Boss Room M" : 10013,
    "Boss Room N" : 10014,
    "Boss Room O" : 10015,
    "Boss Room P" : 10016,
    "Boss Room Q" : 10017,
    "Boss Room R" : 10018,
    "Boss Room S" : 10019,
    "Boss Room T" : 10020,
    "Boss Room U" : 10021,
    "Boss Room V" : 10022,
    "Boss Room W" : 10023,
    "Boss Room X" : 10024,
    "Boss Room Y" : 10025,
    "Boss Room Z" : 10026,
    "Boss Room a" : 10027,
    "Boss Room b" : 10028,
}
define TYPES_OF_TOKEN = [
    "Rest Token",
    "Ancestry Feat Token",
    "General Feat Token",
    "Skill Training Token",
    "Weapon Token",
    "Armor Token",
    "Shield Token",
    "Wand Token",
    "Staff Token",
    "Magic Item Token",
    "Consumable Token",
    "Apex Item Token",
    "Property Rune Token",
    "Material Token",
    "Healing Potion Token",
    "Elixir of Life Token"
]
define TYPES_OF_KEY = [
    "Red Key",
    "Blue Key",
    "Green Key",
    "Yellow Key",
    "Cyan Key",
    "Magenta Key",
    "White Key",
    "Black Key",
    "Gray Key",
    "Orange Key",
    "Azure Key",
    "Chartreuse Key",
    "Teal Key",
    "Violet Key",
    "Pink Key",
    "Amber Key",
    "Indigo Key",
    "Purple Key",
    "Crimson Key",
    "Vermilion Key"
]
define TYPES_OF_UNLOCK = [
    "Avoid Notice Unlock",
    "Defend Unlock",
    "Detect Magic Unlock",
    "Repeat a Spell Unlock",
    "Scout Unlock",
    "Search Unlock",
    "Sustain an Effect Unlock",
    "Cover Tracks Unlock",
    "Hustle Unlock",
    "Investigate Unlock",
    "Track Unlock"
]


label after_load:
    # This ensures that the victory file gets rewritten to connections if it somehow got missed
    if victory_achieved:
        python:
            if not renpy.loadable("victory", directory=CONNECTIONS_PATH):
                with open(os.path.join(CONNECTIONS_PATH, "victory"), 'w') as f:
                    f.close()
    return

label receive_items (items=[1]):
    # This is called by the get_items function in ap_engine.rpy. It just calls receive_item for all the new items
    while items:
        call receive_item(items.pop(0)) from _call_recieve_item
    return

label receive_item (item=1):
    # This is only called by receive_items; it gives the passed item to the player
    # Add functionality in the next line if needed
    python:
        if ID_TO_ITEM_NAME[item] in inventory:
            inventory[ID_TO_ITEM_NAME[item]] += 1
        else:
            inventory[ID_TO_ITEM_NAME[item]] = 1
    if not receive_silently:
        show screen get_item(ID_TO_ITEM_NAME[item]) with moveintop
        "{nw}"
    return

label victory:
    # This is called when the victory condition has been met
    python:
        victory_achieved = True
        with open(os.path.join(CONNECTIONS_PATH, "victory"), 'w') as f:
                f.close()
    return

label file_error:
    # This is called if there's something gone wrong with the files
    "One or more files are missing. Make sure that you have the AP Pathfinder 2e Client running and connected to your room and slot."
    $ renpy.set_return_stack([])
    return
    

screen get_item(message):
    # This screen displays what item has just been received.

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _("Recieved [message]!"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("OK") action Hide(None, moveoutbottom)

    ## Right-click and escape also close.
    key "game_menu" action Hide(None, moveoutbottom)

screen progression_watcher():
    # This screen is a constantly running watcher for locations to send to Archipelago and for items received from Archipelago

    timer 0.5 action Function(game_watcher) repeat True

screen inventory_button():
    # This screen shows the button to check the player's inventory

    zorder 10

    frame:
        at topright
        at transform:
            offset(-5, 80)
        vbox:
            textbutton "Inventory" action Show("inventory_screen")

screen inventory_screen():
    # This screen shows the player's currently held tokens, unlocks, and keys
    zorder 15
    modal True
    tag inventory_screens

    frame:
        at transform:
            xalign 0.5
            yalign 0.5
        vbox:
            textbutton "Tokens" action Show("tokens_screen") xalign 0.5
            textbutton "Keys" action Show("keys_screen") xalign 0.5
            if include_exploration_activities:
                textbutton "Unlocks" action Show("unlocks_screen") xalign 0.5
            textbutton "Close" action Hide("inventory_screen") xalign 0.5

screen tokens_screen():
    # This screen shows the player's currently held tokens
    zorder 15
    modal True
    tag inventory_screens

    frame:
        at transform:
            xalign 0.5
            yalign 0.5
        vbox:
            grid 4 4:
                spacing 10
                for token in TYPES_OF_TOKEN:
                    if token in inventory:
                        if inventory[token] > 0:
                            textbutton "[token]: [inventory[token]]" action Confirm("Use the token?", Function(use_token, token)) xalign 0.5
                        else:
                            text "[token]: [inventory[token]]" xalign 0.5
                    else:
                        text "??? Token" xalign 0.5
            
            textbutton "Close" action Show("inventory_screen") xalign 0.5

screen keys_screen():
    # This screen shows the player's currently held keys
    zorder 15
    modal True
    tag inventory_screens

    frame:
        at transform:
            xalign 0.5
            yalign 0.5
        vbox:
            grid 4 5:
                spacing 5
                for k in TYPES_OF_KEY:
                    if k in inventory:
                        text k xalign 0.5
                    else:
                        text "??? Key" xalign 0.5
            
            textbutton "Close" action Show("inventory_screen") xalign 0.5

screen unlocks_screen():
    # This screen shows the player's currently held unlocks
    zorder 15
    modal True
    tag inventory_screens

    frame:
        at transform:
            xalign 0.5
            yalign 0.5
        vbox:
            grid 2 7:
                transpose True
                spacing 10

                for u in TYPES_OF_UNLOCK:
                    if u in inventory:
                        text u xalign 0.5
                    else:
                        text "??? Unlock" xalign 0.5
                
                for _ in range(3):
                    text "" xalign 0.5
            
            textbutton "Close" action Show("inventory_screen") xalign 0.5


screen stat_screen():
    # This screen displays the characters' current level and runes at the top of the screen
    zorder 10

    frame:
        at transform:
            pos (5, 10)
            xalign 0.5
        hbox:
            text "Level [inventory['Level Up'] + 1]"
            null width 20
            if not use_abp:
                if inventory["Progressive Weapon Rune"] == 0:
                    text "Normal Weapons"
                elif inventory["Progressive Weapon Rune"] == 1:
                    text "+1 Weapons"
                elif inventory["Progressive Weapon Rune"] == 2:
                    text "+1 Striking Weapons"
                elif inventory["Progressive Weapon Rune"] == 3:
                    text "+2 Striking Weapons"
                elif inventory["Progressive Weapon Rune"] == 4:
                    text "+2 Greater Striking Weapons"
                elif inventory["Progressive Weapon Rune"] == 5:
                    text "+3 Greater Striking Weapons"
                elif inventory["Progressive Weapon Rune"] >= 6:
                    text "+3 Major Striking Weapons"
                null width 20
                if inventory["Progressive Armor Rune"] == 0:
                    text "Normal Armor"
                elif inventory["Progressive Armor Rune"] == 1:
                    text "+1 Armor"
                elif inventory["Progressive Armor Rune"] == 2:
                    text "+1 Resilient Armor"
                elif inventory["Progressive Armor Rune"] == 3:
                    text "+2 Resilient Armor"
                elif inventory["Progressive Armor Rune"] == 4:
                    text "+2 Greater Resilient Armor"
                elif inventory["Progressive Armor Rune"] == 5:
                    text "+3 Greater Resilient Armor"
                elif inventory["Progressive Armor Rune"] >= 6:
                    text "+3 Major Resilient Armor"
                null width 20
            if inventory["Progressive Shield Rune"] == 0:
                text "Normal Shields"
            elif inventory["Progressive Shield Rune"] == 1:
                text "Minor Reinforcing Shields"
            elif inventory["Progressive Shield Rune"] == 2:
                text "Lesser Reinforcing Shields"
            elif inventory["Progressive Shield Rune"] == 3:
                text "Moderate Reinforcing Shields"
            elif inventory["Progressive Shield Rune"] == 4:
                text "Greater Reinforcing Shields"
            elif inventory["Progressive Shield Rune"] == 5:
                text "Major Reinforcing Shields"
            elif inventory["Progressive Shield Rune"] >= 6:
                text "Supreme Reinforcing Shields"
            if inventory["Apex Items Token"] >= 1 and not use_abp:
                null width 20
                text "Apex Items"