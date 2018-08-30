import sqlite3
import sys

conn = sqlite3.connect(sys.argv[1])
print(conn.execute("select (author_gender) FROM papers where paper_id='6e8dd3bbc8c6dc2b170028a0afe376f1e9decb25'").fetchall())
