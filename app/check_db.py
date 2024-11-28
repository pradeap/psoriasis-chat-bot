import sqlite3

# Path to the SQLite database
db_path = r"D:\Pradeep\cv\2024\inizio\fast_api_py_1\pythonProject\psoriasis.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to fetch all rows from the `publication` table
cursor.execute('SELECT id, topic, abstract, content FROM publication')
rows = cursor.fetchall()

# Display the data
print(f"{'ID':<5} {'Topic':<50} {'Abstract':<100} {'Content':<100}")
print("-" * 180)
for row in rows:
    id, topic, abstract, content = row
    print(f"{id:<5} {topic[:50]:<50} {abstract[:100]:<100} {content[:100]:<100}")  # Adjust spacing if needed

# Close the connection
conn.close()
