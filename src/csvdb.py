import csv
import sqlite3
import sys
from tqdm import tqdm
import mmap

class CSVDB:
    def __init__(self, filename, header=True, delimiter=","):
        self.filename = filename
        self.con = sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
        self.cur = self.con.cursor()
        with open(self.filename, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            if header:
                header = next(reader)
                columns = [h.strip() for h in header]
            else:
                print("--header=False is currently not implemented")
                sys.exit()
            self.cur.execute(f"CREATE TABLE t {str(header).replace('[', '(').replace(']', ')')}")
            
            self.cur.execute("SELECT * from t")

            query = "INSERT INTO t({0}) VALUES ({1})"
            query = query.format(','.join(columns), ','.join('?' * len(columns)))

            row_length = 0

            for row in tqdm(reader, total=_get_num_lines(filename)):
                self.cur.execute(query, row)
                row_length+=1
            self.con.commit()
            print(f"Loaded file: {filename}")
            print(f"Columns: {len(columns)}")
            print(f"Rows: {row_length}")

def _get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines