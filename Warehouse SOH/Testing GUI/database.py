import sqlite3

class Database:
    def __init__(self, db_name="warehouse_inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the inventory table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id BIGSERIAL PRIMARY KEY,
            raw_code TEXT,
            whse1_buo REAL,
            whse1_excess REAL,
            whse2_buo REAL,
            whse2_excess REAL,
            whse4_buo REAL,
            whse4_excess REAL,
            whse1_terumo REAL,
            whse1_prepare REAL,
            in_value REAL,
            out_value REAL,
            cons REAL,
            gain REAL,
            loss REAL,
            ending_balance REAL,
            status TEXT
        )
        """)
        self.conn.commit()

    def execute_query(self, query, params=None):
        """Execute a query with optional parameters."""
        if params is None:
            return self.cursor.execute(query)
        return self.cursor.execute(query, params)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()