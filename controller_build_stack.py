from controller_db_write import *
from controller_db_read import *


def build_stack(included_player_numbers, excluded_player_numbers):
    all_players = get_players_from_table()
    print_rosters = all_players
    if len(excluded_player_numbers) > 0:
        print("The following players will be excluded:")
        excluded_players = get_player_array(excluded_player_numbers, all_players)
    else:
        excluded_players = []
    if len(included_player_numbers) > 0:
        print("The following players will be included:")
        included_players = get_player_array(included_player_numbers, all_players)
    else:
        included_players = []
    if len(excluded_players) > 0:
        print("Filtering all of the excluded players... ")
    for element in excluded_players:
        if print_rosters:
            temp = [element]
            print("Preparing to exclude " + element[0])
            add_to_table("excluded_players", temp)
            print_rosters = filter_array([], temp)
        else:
            break
    if len(included_players) > 0:
        print("Filtering all of the included players... ")
    for element in included_players:
        if print_rosters:
            temp = [element]
            print("Preparing to include " + element[0])
            add_to_table("included_players", temp)
            print_rosters = filter_array(temp, [])
        else:
            initialize_current_table("", "")
            break
    if print_rosters:
        count = get_count('current')
        print("Complete!  This combination yielded " + str(count) + " rosters")
        return "This stack has " + str(count) + " valid rosters.  Press Write CSV to create a file"
    else:
        return "This combinations did not yield any valid rosters, please try again"


def get_player_array(user_input, plyr_list):
    players = []
    for element in user_input:
        index = int(element)-1
        if plyr_list[index] not in players:
            players.append([plyr_list[index]])
            print(plyr_list[index])

    return players
