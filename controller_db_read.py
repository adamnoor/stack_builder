import sqlite3


def get_count(table):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    if int(cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + table + "';").fetchall()[0][
               0]) > 0:

        select_statement = "SELECT COUNT(*) FROM " + table
        return int(cur.execute(select_statement).fetchall()[0][0])
    else:
        return 0


def get_max(table, column):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    if int(cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + table + "';").fetchall()[0][
               0]) > 0:
        select_statement = "SELECT MAX(" + column + ") FROM " + table
        return cur.execute(select_statement).fetchall()[0][0]
    else:
        return 0


def get_all_rosters():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    select_statement = "SELECT * FROM roster ORDER BY ratio DESC"
    return cur.execute(select_statement).fetchall()


def get_last_updated():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    if int(cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='last_update';").fetchall()[0][
               0]) > 0:

        select_statement = "SELECT date FROM last_update"
        return cur.execute(select_statement).fetchall()[0][0]
    else:
        return "There are no tables                   "


def show_players_as_list():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    if int(cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='last_update';").fetchall()[0][
               0]) > 0:

        select_statement = "SELECT name FROM players"
        lcl_str = ""
        temp = cur.execute(select_statement).fetchall()
        count = 1
        for element in temp:
            lcl_str = lcl_str + str(count) + ") " + element[0] + " "

            if count % 2 == 0 and count >= 2:
                lcl_str = lcl_str + "\n"
            count += 1

        return lcl_str
    else:
        return "There are no players"


def get_players_from_table():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    players = []
    player_objects = cur.execute('''
        SELECT name_id FROM players
    ''')

    for element in player_objects:
        players.append(element[0])

    return players


def check_current_table():
    conn = sqlite3.connect('football.sqlite')
    c = conn.cursor()
    # get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='current' ''')
    if c.fetchone()[0] == 1:
        return True
    else:
        return False
