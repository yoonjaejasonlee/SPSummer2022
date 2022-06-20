import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="a1234567!",
        host="sparrow-ml.fasoo.com",
        port=30198,
        database="Analyzer"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)

cur = conn.cursor()

insert_query = "INSERT INTO analyze_results (num_files, min_CCN, max_CCN, average_CCN, total_LOC) " \
               "VALUES (111, 2, 3, 4, 4) "

try:
    cur.execute(insert_query)
except mariadb.Error as e:
    print(f"Error: {e}")

conn.commit()
