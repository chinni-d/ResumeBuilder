import pymysql

# Connect to MySQL
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',  # Change to your MySQL password
        database='resume_builder'
    )
    cursor = conn.cursor()
    
    # Show all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if tables:
        print("Tables found:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found. Run your Flask app first to create tables.")
    
    conn.close()
    
except pymysql.Error as e:
    print(f"MySQL Error: {e}")
    print("Make sure MySQL is running and credentials are correct.")