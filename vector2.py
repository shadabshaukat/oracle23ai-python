import oracledb
import os
import openai
import numpy

# Get your OpenAI API Key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create the vector embedding [a JSON object]
response = openai.Embedding.create(
  model="text-embedding-ada-002",
  input="The food was delicious and the waiter..."
)

# Extract the vector from the JSON object
vec = response['data'][0]['embedding']

# Verify the number of dimensions in the vector
print(len(vec))

# Connect to your Oracle 23.4 database
connection = oracledb.connect(user="ADMIN", password="", dsn="myadw_high", config_dir="/Users/shadab/Downloads/wallet_adb_free_container/tls_wallet", wallet_location="/Users/shadab/Downloads/wallet_adb_free_container/tls_wallet", wallet_password="")

cursor = connection.cursor()

# Make sure to use a table with the correctly size vector
cursor.execute("""
    begin
        execute immediate 'drop table open_ai';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

cursor.execute("""
    create table open_ai (
        id number,
        v vector(1536, float32),
        primary key (id))""")

cursor.setinputsizes(None, oracledb.DB_TYPE_VECTOR)

# Insert the vector using the bind variable from the generated vector
id_val = 1
cursor.execute("insert into open_ai values (:1, :2)", [id_val, vec])

# Retrieve the vector
cursor.execute('select * from open_ai')
for row in cursor:
     print(row)

connection.commit()
connection.close()
print("Bye bye ")
