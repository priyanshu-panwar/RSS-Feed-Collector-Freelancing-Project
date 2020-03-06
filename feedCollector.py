import sqlite3
from sqlite3 import Error
import feedparser
import sys
 
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        sys.exit()
    return conn

def write_query(conn):
    cursor = conn.cursor()
    sql = '''CREATE TABLE FEED(
        TITLE TEXT,
        DATE_PUBLISHED DATETIME,
        SOURCE TEXT,
        MESSAGE TEXT
    )'''
    cursor.execute(sql)

def feedParser(conn, url):
    data = feedparser.parse(url)
    cursor = conn.cursor()
    #print(d.feed.title)
    #print(d.feed.link)
    for d in data.entries:
        title = None
        if d.title:
            title = d.title
        date = None
        if d.published:
            date = d.published
        message = None
        if d.description:
            message = d.description
        link = None
        if d.link:
            link = d.link
        query = """INSERT INTO FEED VALUES(?, ?, ?, ?)"""
        record = (title, date, link, message)
        cursor.execute(query, record)
        conn.commit()
        print("Data inserted...")

def showParsed(conn):
    cursor = conn.cursor()
    for i in cursor.execute("""SELECT * FROM FEED"""):
        print(i)

def main():
    database = r"database.db"
    conn = create_connection(database)

    link = 'https://bobbycodes.code.blog/feed/'
    
    if(conn):
        print("connected...")
        print("Running sql query to create table...")
        write_query(conn)
        print("Done...")
    else:
        print("Error")
        sys.exit()
    feedParser(conn, link)
    #showParsed(conn)

if __name__ == '__main__':
    main()
