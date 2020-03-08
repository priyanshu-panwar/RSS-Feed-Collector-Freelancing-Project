import sqlite3
from sqlite3 import Error
import feedparser
import sys
import csv
import datetime

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        sys.exit()
    return conn

def feedParser(conn, url):
	d = feedparser.parse(url)
	cursor = conn.cursor()
	#---channel entities---
	channel_title = d.feed.title
	channel_url = None
	channel_url = d.feed.link
	#---item entities---
	for i in d.entries:
		id_ = i.id
		title = i.title
		category = i.category
		link = None
		link = i.link
		description = i.description
		pubdate = None
		pubdate = i.published
		json = str(i)
		query = """INSERT INTO RSS_ITEMS(CHANNEL_URL, CHANNEL_TITLE, ITEM_ID, ITEM_TITLE, ITEM_CATEGORY, ITEM_LINK, ITEM_DESCRIPTION, ITEM_PUBDATE, ITEM_FULL_JSON) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
		record = (channel_url, channel_title, id_, title, category, link, description, pubdate, json)
		cursor.execute(query, record)
		conn.commit()
		print(f"Entry made of {link}")
		#---Now log table entities---
		datetime_of_run = datetime.datetime.now()
		success = True
		failReason = None
		if link==None:
			success = False
		if success==False:
			failReason = 'Link Expired'
		query = """INSERT INTO LOG_ITEMS(URL, SUCCESS, DATERUN, FAILREASON) VALUES(?, ?, ?, ?)"""
		record = (link, success, datetime_of_run, failReason)
		cursor.execute(query, record)
		conn.commit()
		print("Log entry made...")

def main():
    database = r"database.db"
    conn = create_connection(database)

    #link = 'https://bobbycodes.code.blog/feed/'
    
    if(conn):
        print("connected to database...")
    else:
        print("Error in connection...")
        sys.exit()
    #feedParser(conn, link)

    with open('links.csv') as csv_file:
    	csv_reader = csv.reader(csv_file)
    	for row in csv_reader:
    		link = row[0]
    		print(link)
    		feedParser(conn, link)

if __name__ == '__main__':
    main()
