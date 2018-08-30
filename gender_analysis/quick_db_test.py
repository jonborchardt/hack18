import sqlite3
import sys
paper_id = "cfa06e42e057801131f757d7e520c39b6893a83a"
print ("loading...")
conn = sqlite3.connect(sys.argv[1])
print ("searching...")
print(conn.execute("select (author_gender) FROM papers where paper_id='{}'".format(paper_id)).fetchall())
print(conn.execute("select (author_gender) FROM papers where paper_id='{}'".format(paper_id)).fetchall())
