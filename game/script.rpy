label start:

    $ read_files()
    $ get_items()
    # This makes items announce that they have been received. It starts True so that the initial
    # items (Level Ups and Runes that are sent from starting at a higher level than 1) don't flood the player
    $ receive_silently = False

    # This is a timer that runs the function that checks for new locations checked and items received
    show screen progression_watcher
    # This shows the characters' stats
    show screen stat_screen
    # This shows a button to let the player see their inventory
    show screen inventory_button

    "Welcome to AP Pathfinder 2e!"
    "Your starting Ancestries are: [starting['Ancestries']]"
    "Your starting Backgrounds are: [starting['Backgrounds']]"
    "Your starting Classes are: [starting['Classes']]"
    "Your starting weapons are: [starting['Weapons']]"
    "Your starting armors are: [starting['Armors']]"
    if starting["Shields"]:
        "Your starting shields are: [starting['Shields']]"

label entrance:

    "You are at the entrance. From here, you can only move forward to Room 1."

    call room("Room 1", "Entrance")

    jump entrance

label room(room_name="Room 1", source="Entrance"):

    menu .menu_1:
        "You are in [room_name]. What would you like to do?"

        "Fight" if not (room_name + " A") in checked:

            "This fight is [rooms[room_name]['Difficulty']] [rooms[room_name]['Level']]."

            $ can_fight = requirements_by_level(int(rooms[room_name]['Level']))

            if strict_logic and not can_fight:

                "You are not yet prepared for this fight."
                jump .menu_1
            
            menu:
                "Do you want to do this fight?"

                "Yes":
                    "The following enemies are ready to fight:"
                    $ enemies = ", ".join(rooms[room_name]['Creatures'])
                    "[enemies]"

                    menu:
                        "Did you win?"

                        "Yes":
                            python:
                                for letter in "ABCDE":
                                    checked.append(f"{room_name} {letter}")
                            "Congratulations!"
                            jump .menu_1

                        "No":
                            "Try again later when you are better prepared."
                            jump .menu_1

                "No":
                    jump .menu_1

        "Continue" if rooms[room_name]["Doors"]:
            python:
                doors = []

                for i in range(len(rooms[room_name]["Doors"])):
                    doors.append((rooms[room_name]["Doors"][i], i))
                
                doors.append(("Stay Here", -1))

                narrator("Where would you like to go?", interact=False)
                result = renpy.display_menu(doors)
            
            if result == -1:
                jump .menu_1
            
            if rooms[room_name]["Doors"][result] == "Boss Room":
                $ boss = "the "
            else:
                $ boss = ""

            if rooms[room_name]["Keys"][result]:
                if rooms[room_name]["Keys"][result] not in inventory:
                    "You need the [rooms[room_name]['Keys'][result]] to go to [boss][rooms[room_name]['Doors'][result]]. Come back when you have it."
                    jump .menu_1

                else:
                    "You use the [rooms[room_name]['Keys'][result]] to open the door."
                    if not boss:
                        call room(rooms[room_name]['Doors'][result], room_name)
                    else:
                        call boss_room(room_name)
                    jump .menu_1

            if not boss:
                call room(rooms[room_name]['Doors'][result], room_name)
            else:
                call boss_room(room_name)
            jump .menu_1


        "Return to [source]":
            return

label boss_room(source="Room 1"):

    menu .menu_1:
        "You are in the Boss Room. What would you like to do?"

        "Fight" if not victory_achieved:

            "This fight is [rooms['Boss Room']['Difficulty']] [rooms['Boss Room']['Level']]."

            $ can_fight = requirements_by_level(int(rooms['Boss Room']['Level']))

            if strict_logic and not can_fight:

                "You are not yet prepared for this fight."
                jump .menu_1
            
            menu:
                "Do you want to do this fight?"

                "Yes":
                    "The following enemies are ready to fight:"
                    $ enemies = ", ".join(rooms['Boss Room']['Creatures'])
                    "[enemies]"

                    menu:
                        "Did you win?"

                        "Yes":
                            python:
                                receive_silently = True

                                for letter in rooms["Boss Room"]["Locations Needed"]:
                                    checked.append(f"Boss Room {letter}")
                            call victory
                            "Congratulations! You have completed the game! Feel free to continue exploring to your heart's content."
                            $ receive_silently = False
                            jump .menu_1

                        "No":
                            "Try again later when you are better prepared."
                            jump .menu_1

                "No":
                    jump .menu_1

        "Return to [source]":
            return

