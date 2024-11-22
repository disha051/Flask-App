import sqlite3 
# to create a database and to create a table
conn = sqlite3.connect('insurance.db')

query = """
create table project 
(age integer ,gender integer , bmi integer , children integer , region varchar(5),
smoker integer , health integer , prediction varchar(10))"""

query_to_fetch = """
select * from project
"""

# to create table 
cur = conn.cursor()  # cursor sql 
# cur.execute(query)
# print("Your database and your table is created!")

# to fetch the data from database 
cur.execute(query_to_fetch)
for record in cur.fetchall():
    print(record)


cur.close()
conn.close()