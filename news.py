#!/usr/bin/env python3
#
# Reporting tool for the newspaper database.

import datetime
import time
import psycopg2

DBNAME = "news"
DASH = '-' * 60


def pop_articles():
    """Return the most popular three articles of all time."""
    # Try to connect
    try:
        conn = psycopg2.connect(database=DBNAME)
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    cursor = conn.cursor()
    cursor.execute("""select articles.title, log.views
                      from articles inner join (
                        select log.path, count(log.path) as views
                        from log group by log.path
                      ) as log
                      on concat('/article/', articles.slug) = log.path
                      order by log.views desc limit 3;""")
    rows = cursor.fetchall()
    print(DASH)
    print("1. What are the most popular three articles of all time?")
    print(DASH)
    for row in rows:
        print "%s -- %s views \n" % row
    conn.close()


def pop_authors():
    """Return the list of authors
       sorted by the number of views each author gets"""
    # Try to connect
    try:
        conn = psycopg2.connect(database=DBNAME)
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    cursor = conn.cursor()    
    cursor.execute("""select authors.name, author_view.views
                      from authors inner join author_view
                      on authors.id = author_view.author
                      order by author_view.views desc;""")
    rows = cursor.fetchall()
    print(DASH)
    print("2. Who are the most popular article authors of all time?")
    print(DASH)
    for row in rows:
        print "%s -- %s views \n" % row
    conn.close()


def status_check():
    """Return the list of dates when more than 1% of requests led to error"""
    # Try to connect
    try:
        conn = psycopg2.connect(database=DBNAME)
    except (Exception, psycopg2.DatabaseError) as error:
        print (error)
    cursor = conn.cursor()    
    # List the dates when more than 1% of requests led to error
    cursor.execute("""select date_total.date,
                      (date_error.error*100/date_total.total) as percent
                      from date_total inner join date_error
                      on date_total.date = date_error.date
                      and (date_error.error*100/date_total.total) > 1
                      order by percent desc;""")
    rows = cursor.fetchall()
    print(DASH)
    print ("3. On which days did more than 1% of requests lead to errors?")
    print(DASH)
    for row in rows:
        print "%s - %.1f %% errors" % (row[0].strftime('%d %b, %Y'), row[1])
    conn.close()


pop_articles()
pop_authors()
status_check()
