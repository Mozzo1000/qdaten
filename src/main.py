
import argparse
import sqlite3
from prettytable import from_db_cursor
from csvdb import CSVDB
import time
import humanize
import datetime as dt
from tui import TUI

def main():
    parser = argparse.ArgumentParser(description="CSV to SQL Explorer")
    parser.add_argument("file", type=str, help="CSV file")
    parser.add_argument("--delimiter", type=str, default=",", help="Delimiter used in the csv file")
    parser.add_argument("--header", action="store_true", default=True, help="Use if CSV file does not have a header row")
    parser.add_argument("-c", type=str, default="", help="Run SQL query directly against CSV without any TUI")
    parser.add_argument("--no-default-query", action="store_true", default=False, help="Do not run SELECT from table query when starting in interactive mode")
    args = parser.parse_args()

    if args.file:
        db = CSVDB(args.file, args.header, args.delimiter)

        if args.c:
            try:
                _start_execute_time = time.time()
                db.cur.execute(args.c)
                table = from_db_cursor(db.cur)
                print(table)
                print(f"Returned {len(table.rows)} row(s) in {_exec_time_format(time.time() - _start_execute_time)}")

            except sqlite3.OperationalError as error:
                print(f"Invalid SQL\n {error}")
        else:
            tui = TUI(args, db)
            tui.run()

        db.con.close()

def _exec_time_format(seconds):
    if seconds >= 60:
        return humanize.naturaldelta(dt.timedelta(seconds=seconds))
    else:
        return f"{round(seconds, 2)} seconds"


if __name__ == "__main__":
    main()