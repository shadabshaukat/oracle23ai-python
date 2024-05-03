import array
import oracledb

connection = oracledb.connect(user="ADMIN", password="", dsn="myadw_high", config_dir="/Users/shadab/Downloads/wallet_adb_free_container/tls_wallet", wallet_location="/Users/shadab/Downloads/wallet_adb_free_container/tls_wallet", wallet_password="")

print("Connected to Oracle Database")

cursor = connection.cursor()

cursor.execute("""
    begin
        execute immediate 'drop table t1';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

cursor.execute("""
    create table t1 (
      ID     NUMBER,
      VCOL   VECTOR(3),
      VCOL32 VECTOR(3, FLOAT32),
      VCOL64 VECTOR(3, FLOAT64),
      VCOL8  VECTOR(3, INT8),
      PRIMARY KEY (id))""")

# Bind variable values
id_val = 1
vector_val = [5.3, 2.4, 3.1412]
vector_data_32 = array.array('f', [1.625, 2.5, 3.0])	     # 32-bit float
vector_data_64 = array.array('d', [4.25, 5.75, 6.5])	     # 64-bit float
vector_data_8  = array.array('b', [7, 8, 9])	             # 8-bit signed integer

cursor.setinputsizes(None, oracledb.DB_TYPE_VECTOR)
cursor.execute("insert into t1 values (:1, :2, :3, :4, :5)",
               [id_val,
                vector_val,
                vector_data_32,
                vector_data_64,
                vector_data_8])
connection.commit()

cursor.execute('select * from t1')
for row in cursor:
     print(row)

connection.close()
print("Disconnected from Oracle Database")
