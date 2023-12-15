import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

sql_path = os.path.join(os.getcwd(), 'sql/init.sql')

with open(sql_path, 'r') as file:
    sql_script = file.read().replace('**TEMPLATE_DB_PASS**', os.getenv('DB_PASS'))

print('connecting...')

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('PG_USER'),
    password=os.getenv('PG_PASS'),
    host='localhost',
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()
print('executing...')
cur.execute(sql_script)
conn.commit()
cur.close()
conn.close()
print('init complete.')
