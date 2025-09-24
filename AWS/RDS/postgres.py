import psycopg2

db_host = 'trueeval.chwgcyowk8ty.us-east-2.rds.amazonaws.com'
db_name = 'trueeval'
db_user = 'postgres'
db_pass = 'Otani30!'

connection = psycopg2.connect (host = db_host, database = db_name, user = db_user, password = db_pass)
print("Connected to database")

cursor = connection.cursor()
cursor.execute('SELECT VERSION()')
db_version = cursor.fetchone()
print(db_version)

cursor.close()
