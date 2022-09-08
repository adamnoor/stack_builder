from controller_db_read import *
from controller_db_write import *


def create_stacks_table(qb_num, dst_num, inc_num_array, exc_num_array):
    players = get_players_from_table()
    dst = ""
    included_players = []
    excluded_players = []
    if qb_num == "":
        return False
    quarterback = players[qb_num]
    if dst_num != "":
        dst = players[dst_num]
    if inc_num_array:
        for element in inc_num_array:
            included_players.append(players[int(element) - 1])
    if exc_num_array:
        for element in exc_num_array:
            excluded_players.append(players[int(element) - 1])
    write_stacks_table(quarterback, dst, included_players, excluded_players)
    return True

