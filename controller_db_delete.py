import sqlite3


def drop_tables_if_exists():
    message = "All tables have been dropped"
    conn = sqlite3.connect('football.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS rosters')
    cur.execute('DROP TABLE IF EXISTS current')
    cur.execute('DROP TABLE IF EXISTS players')
    cur.execute('DROP TABLE IF EXISTS last_update')
    return message
