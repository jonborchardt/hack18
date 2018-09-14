from sqlite_manager import Sqlite_Database
import sys

with Sqlite_Database(sys.argv[1], read_only = True) as db:
    unique_venues = db.conn.execute("SELECT count(distinct venue) FROM papers;").fetchall()
    print("#unique venues = {}".format(unique_venues))
