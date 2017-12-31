# "Database code" for the DB Forum.

#import datetime
import psycopg2
import bleach
#POSTS = [("This is the first post.", datetime.datetime.now())]

DBNAME = 'forum'

def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = psycopg2.connect(database = DBNAME)
  cur = conn.cursor()
  query = "select content, time from posts order by time desc;"
  cur.execute(query)
  rows = cur.fetchall()
  conn.close()
  return rows

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  #POSTS.append((content, datetime.datetime.now()))
  conn = psycopg2.connect("dbname=forum")
  cur = conn.cursor()
  query = "insert into posts(content) values(%s);" 
  cur.execute(query, (bleach.clean(content),))
  conn.commit()
  conn.close()


