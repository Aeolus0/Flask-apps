def database_conn(dbname, user, host, password):
	import psycopg2
	try:
		conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
		cur = conn.cursor
		return cur
	except:
		return False

def auth_user(username, password):
	import bcrypt
	try:
		cur = database_conn("Auth", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		cur.execute("SELECT * FROM AUTH WHERE username = {}".format(username))
		username_non_auth = cur.fetchall()
		# i don't think i need this since only one record will be returned password_hash_loc = 0
		if username_non_auth["password_salted"] == bcrypt.hash(password, username_non_auth["password_salted"]):
			return True
		else:
			return False
	except:
		return False

def sign_up_user(username, password, email):
	import bcrypt
	try:
		cur = database_conn("Auth", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		password_salted = bcrypt.hash(password)
		cur.execute("INSERT INTO Auth(username) values ({})".format(username))
		cur.execute("INSERT INTO Auth(password_salted) values ({})".format(password_salted))
		cur = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1
		cur.execute("INSERT INTO User_info(email) values ({})".format(email))
		return True
	except:
		return False

def sign_up_user_details(name):
	try:
		cur = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1
		cur.execute("INSERT INTO User_info(name) values ({})".format(name))
		return True
	except:
		return False


def shared_presentation(pres_uid, account_or_email):

