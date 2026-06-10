import json
import sqlite3
from pathlib import Path

class JsonToSql:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.path = Path(self.filepath)
        self.conn = sqlite3.connect(f"converted_{self.filepath}.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dictionary(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            word TEXT UNIQUE NOT NULL,
                            meaning TEXT NOT NULL,
                            type TEXT
                )
        """)
        

    def json_data(self) -> dict:
        # extracting the data from the json file
        content = json.loads(self.path.read_text())
        return content

    def push_to_sql(self,pair : tuple) -> None:
        #pushing the data to sql db
        self.cursor.execute("""
            INSERT INTO dictionary(word,meaning)
                            VALUES(?,?)
        """,(pair[0],pair[1]))
        self.conn.commit()


    def data_conversion(self,data: dict) -> None:
        # convert the data to the tuples to push to the sql
        count = 0
        for word,meaning in data.items():
            self.push_to_sql((word,meaning))
            count+=1
        print(f"Conversion completed...\ntotal {count} rows pushed.")
        

    def test_db(self):
        self.cursor.execute("""
        SELECT id, word, meaning FROM dictionary
        """)
        rows = self.cursor.fetchall() # stored as list of tuples
        for row in rows:
            print(f"{row[0]}: {row[1]}  - {row[2]}")

converter = JsonToSql('dictionary.json')
converter.test_db()