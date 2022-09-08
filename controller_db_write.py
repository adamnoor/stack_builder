import csv
import os
import sqlite3
from datetime import datetime


def drop_all_tables():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS rosters')
    cur.execute('DROP TABLE IF EXISTS stacks')
    cur.execute('DROP TABLE IF EXISTS players')
    cur.execute('DROP TABLE IF EXISTS last_update')
    cur.execute('DROP TABLE IF EXISTS qb_dst')
    cur.execute('DROP TABLE IF EXISTS flex')
    return True


def drop_one_table(table):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS "' + table + '"')
    return True


def write_player_table(players):
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


def write_qb_dst_combo_table(qb_dst):
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


def write_flex_combo_table(flex):
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


def write_rosters_table():
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


def write_last_update_table():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS last_update')
    cur.execute('CREATE TABLE last_update ("date" DATETIME)')
    insert_records = "INSERT INTO last_update (date) VALUES(?) "
    now = [[datetime.now().strftime('%Y-%m-%d %H:%M:%S')]]
    cur.executemany(insert_records, now)
    conn.commit()


def write_stacks_table(qb, dst, inc, exc):
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    from_clause = "SELECT * FROM rosters "
    if qb == "":
        return "A quarterback selection is required to build a stack"
    where_clause = " WHERE qb = '" + qb + "'"
    if dst != "":
        where_clause = where_clause + ' AND dst = "' + dst + '"'
    if inc:
        for element in inc:
            where_clause = where_clause + ' AND "' + element + '" IN (rb1, rb2, wr1, wr2, wr3, te, fx)'

    if exc:
        for element in exc:
            where_clause = where_clause + ' AND "' + element + '" NOT IN (rb1, rb2, wr1, wr2, wr3, te, fx)'

    select_statement = from_clause + where_clause
    drop_one_table("stacks")
    cur.execute("CREATE TABLE stacks AS " + select_statement).fetchall()
    return "The stacks have been built, select 'Get Statistics' button to see results"


def write_rosters_to_csv():
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    now = str(datetime.now())
    new_path = r'output_files'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    cur.execute("SELECT * from stacks ORDER BY ratio DESC")
    path = "output_files/Final_Roster_" + str(now) + ".csv"
    with open(path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)
    return "The CSV file has been written and is located in the output_files folder"
