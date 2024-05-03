import oracledb
conn = oracledb.connect(user="ADMIN", password="", dsn="myadw_high", config_dir="/Users/shadab/Downloads/wallet_adb_free_container/tls_wallet", wallet_location="/Users/shadab/Downloads/wallet_adb_free_container/tls_wallet", wallet_password="WelcomeP@ssword321#_")
cr = conn.cursor()
r = cr.execute("SELECT 1 FROM DUAL")
print(r.fetchall())
