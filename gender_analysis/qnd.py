from sqlite_manager import Sqlite_Database
import sys

with Sqlite_Database(sys.argv[1], read_only = True) as db:
    print("counting venues before 2000...")
    unique_venues = db.conn.execute("SELECT count(distinct venue) FROM papers WHERE year <= 2000 ;").fetchall()
    print("#unique venues = {}".format(unique_venues))

    print("counting venues after 2000...")
    unique_venues = db.conn.execute("SELECT count(distinct venue) FROM papers WHERE year > 2000 ;").fetchall()
    print("#unique venues = {}".format(unique_venues))
