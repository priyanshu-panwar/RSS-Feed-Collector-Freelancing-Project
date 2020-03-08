import sqlite3
from sqlite3 import Error
import sys

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        sys.exit()
    return conn

def create_table_rss(conn):
    cursor = conn.cursor()
    sql = '''CREATE TABLE RSS_ITEMS(
        CHANNEL_URL TEXT,
        CHANNEL_TITLE TEXT,
        ITEM_ID TEXT,
        ITEM_TITLE TEXT,
        ITEM_CATEGORY TEXT,
        ITEM_LINK TEXT,
        ITEM_DESCRIPTION TEXT,
        ITEM_PUBDATE DATETIME,
        ITEM_FULL_JSON TEXT
    )'''
    cursor.execute(sql)

def create_table_log(conn):
    cursor = conn.cursor()
    sql = '''CREATE TABLE LOG_ITEMS(
        URL TEXT,
        DATERUN DATETIME,
        SUCCESS TEXT,
        FAILREASON TEXT
    )'''
    cursor.execute(sql)

def main():
    database = r"database.db"
    conn = create_connection(database)

    if(conn):
        print("Connected to the database...")
        print("Creating Table LOG_TABLE")
        create_table_log(conn)
        print("Creating Table RSS_ITEMS...")
        create_table_rss(conn)
        print("Done Both Tables are created...")
    else:
        print("Error")
        sys.exit()
    conn.close()

if __name__ == '__main__':
    main()
