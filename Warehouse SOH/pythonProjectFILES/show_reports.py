self.cursor.execute("PRAGMA table_info(inventory)")
for row in self.cursor.fetchall():
    print(row)