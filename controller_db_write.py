import csv
import os
import sqlite3
from datetime import datetime


def create_player_table(players):
    temp_player_array = []
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS players')
    cur.execute('''
        CREATE TABLE players (
            "name" TEXT,
            "id" REAL,
            "name_id" TEXT,
            "position" TEXT,
            "budget" REAL,
            "projection" REAL,
            "ratio" REAL
        )
        ''')
    insert_records = "INSERT INTO players (name, id, name_id, position, budget, projection, ratio) VALUES(?, ?, " \
                     "?, ?, ?, ?, ?) "
    for element in players:
        temp_player_array.append(
            [element.name, element.id, element.name_id, element.position, element.salary, element.projection,
             element.ratio])
    cur.executemany(insert_records, temp_player_array)
    conn.commit()


def create_qb_dst_combo_table(qb_dst):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS qb_dst')
    cur.execute('''
                            CREATE TABLE qb_dst (
                                "qb" TEXT,
                                "dst" TEXT,
                                "budget" REAL,
                                "projection" REAL,
                                "ratio" REAL
                            )
                            ''')
    insert_records = "INSERT INTO qb_dst (qb, dst, budget, projection, ratio) VALUES(?, ?, ?, ?, ?)"
    qb_dst_temp = []
    for element in qb_dst:
        qb_dst_temp.append(
            [element.qb.name_id, element.dst.name_id, element.salary, element.projection, element.ratio])
    cur.executemany(insert_records, qb_dst_temp)
    conn.commit()


def create_flex_combo_table(flex):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS flex')
    cur.execute('''
                               CREATE TABLE flex (
                                   "rb1" TEXT,
                                   "rb2" TEXT,
                                   "wr1" TEXT,
                                   "wr2" TEXT,
                                   "wr3" TEXT,
                                   "te" TEXT,
                                   "fx" TEXT,
                                   "budget" REAL,
                                   "projection" REAL,
                                   "ratio" REAL
                               )
                               ''')
    insert_records = "INSERT INTO flex (rb1, rb2, wr1, wr2, wr3, te, fx, budget, projection, ratio) VALUES(?, ?, ?, " \
                     "?, ?, ?, ?, ?, ?, ?) "
    flex_temp = []
    for element in flex:
        flex_temp.append(
            [element.rb1.name_id, element.rb2.name_id, element.wr1.name_id, element.wr2.name_id, element.wr3.name_id,
             element.te.name_id, element.fx.name_id, element.salary, element.projection, element.ratio])
    cur.executemany(insert_records, flex_temp)
    conn.commit()


def create_rosters_table():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS rosters')
    cur.execute('''
                   CREATE TABLE rosters AS 
                       SELECT
                           qb,
                           rb1,
                           rb2, 
                           wr1, 
                           wr2, 
                           wr3, 
                           te, 
                           fx, 
                           dst,
                           qb_dst.budget + flex.budget AS budget,
                           ROUND(qb_dst.projection + flex.projection, 2) AS projection,
                           ROUND(qb_dst.ratio + flex.ratio, 2) AS ratio   
                       FROM qb_dst 
                       CROSS JOIN flex
                       WHERE qb_dst.budget + flex.budget <= 50000
                       ''')


def create_last_update_table():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS last_update')
    cur.execute('CREATE TABLE last_update ("date" DATETIME)')
    insert_records = "INSERT INTO last_update (date) VALUES(?) "
    now = [[datetime.now().strftime('%Y-%m-%d %H:%M:%S')]]
    cur.executemany(insert_records, now)
    conn.commit()


def initialize_current_table(qb, dst):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    where_clause = ""
    if qb != "" and dst != "":
        where_clause = "WHERE qb = '" + qb + "' AND dst = '" + dst + "'"
    print("")
    print("Initializing a local table to include " + qb + " and " + dst + ".  This may take some time...")
    cur.execute('DROP TABLE IF EXISTS current')
    cur.execute('DROP TABLE IF EXISTS included_players')
    cur.execute('DROP TABLE IF EXISTS excluded_players')
    cur.execute("CREATE TABLE current AS SELECT * FROM rosters " + where_clause).fetchall()
    cur.execute('''
    CREATE TABLE included_players (
        "name" TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE excluded_players (
        "name" TEXT
    )
    ''')


def add_to_table(table_name, plyr_list):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    # print("Getting a list of players to " + type + "...")
    cur.execute('DROP TABLE IF EXISTS ' + table_name)
    cur.execute('''
    CREATE TABLE ''' + table_name + ''' (
        "name" TEXT
    )
    ''')
    insert_records = "INSERT INTO " + table_name + " (name) VALUES(?)"
    cur.executemany(insert_records, [plyr_list[len(plyr_list) - 1]])
    conn.commit()
    print("Currently processing " + str(plyr_list[len(plyr_list) - 1][0]))


def filter_array(incl_players, excl_players):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    select_statement = '''
    SELECT 
    qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection, ratio 
    FROM current
    WHERE budget <= ''' + str(50000) + '''  
    '''

    if len(incl_players) > 0:
        select_statement = select_statement + '''AND EXISTS ( SELECT name FROM included_players WHERE name = QB OR 
        name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = DST) '''

    if len(excl_players) > 0:
        select_statement = select_statement + '''AND NOT EXISTS ( SELECT name FROM excluded_players WHERE name = QB 
        OR name = RB1 or name = RB2 or name = WR1 or name = WR2 or name = WR3 or name = TE or name = FX or name = 
        DST) '''

    select_statement = "WITH t AS (" + select_statement + ") SELECT qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, " \
                                                          "budget, projection, ratio FROM t "
    all_rosters = cur.execute(select_statement).fetchall()

    if len(all_rosters) > 1:
        cur.execute('DROP TABLE IF EXISTS current')
        cur.execute('''
        CREATE TABLE current (
            "qb" TEXT,
            "rb1" TEXT,
            "rb2" TEXT,
            "wr1" TEXT,
            "wr2" TEXT,
            "wr3" TEXT,
            "te" TEXT,
            "fx" TEXT,
            "dst" TEXT,
            "budget" REAL,
            "projection" REAL,
            "ratio" REAL
        )
        ''')

        insert_records = "INSERT INTO current (qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection, " \
                         "ratio) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        cur.executemany(insert_records, all_rosters)
        conn.commit()
        return True
    else:
        print("This restriction doesn't yield any rosters.  Try again.")
        return False


def write_rosters_to_csv():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    now = str(datetime.now())
    new_path = r'output_files'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    cur.execute("SELECT * from current ORDER BY ratio DESC")
    path = "output_files/Final_Roster_" + str(now) + ".csv"
    with open(path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)
    return "The CSV file has been written and is located in the output_files folder"
