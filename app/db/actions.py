
import time
import bcrypt
import psycopg2
import os.path
##########################
###### Fundamentals ######
##########################

def auth_schema():
	auth_schema_var = """CREATE TABLE Auth
	(id INT SERIAL PRIMARY KEY NOT NULL,
	username              TEXT NOT NULL,
	password_salted       TEXT NOT NULL,
	email                 TEXT NOT NULL
	)
	"""
	return auth_schema_var

def user_info_schema():
	user_info_schema_var = """CREATE TABLE User_info
	(id INT SERIAL PRIMARY KEY NOT NULL,
	name                  TEXT NOT NULL,
	location              TEXT NOT NULL,
	github                TEXT NOT NULL,
	linkedin              TEXT NOT NULL,

	)"""
    return user_info_schema_var

def database_conn(dbname, user, host, password):
	try:
		conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
		cur = conn.cursor
		return cur
	except:
		return (False, "Something went wrong in the database bits")

def create_database(root_dir):
	auth_db = root_dir + "app/db/Auth.db"
	user_info_db = root_dir + "app/db/User_info.db"
	if not os.path.isfile(auth_db):
		open(auth_db, 'a').close()
		cur = database_conn("Auth.db", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		cur.execute(auth_schema)
	if not os.path.isfile(user_info_db):
		open(user_info_db, 'a').close()
		cur = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1



##########################
###### Sign in Stuff #####
##########################


def auth_user(user_info):
	try:
		cur = database_conn("Auth.db", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		cur.execute("SELECT * FROM Auth WHERE username = {}".format(user_info["username"]))
		username_non_auth = cur.fetchall()
		password_hash_loc = 2
		if username_non_auth[password_hash_loc] == bcrypt.hashpw(user_info["password"], username_non_auth[password_hash_loc]):
			return True
		else:
			return False
	except:
		return (False, "Unable to establish database connection")

###########################
###### Sign Up Stuff ######
###########################


def sign_up_user(user_info):
	try:
		cur = database_conn("Auth.db", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		password_salted = bcrypt.hashpw(user_info["password"], bcrypt.gensalt())
		if ((cur.execute("SELECT * FROM Auth(username) WHERE username = {}".format(user_info["username"]) != ""))): # TODO: i think i need to expad upon the != "" thing
			return (False, "Username already taken")
		if ((cur.execute("SELECT * FROM Auth(email) WHERE email = {}".format(user_info["email"]) != ""))): # TODO: i think i need to expad upon the != "" thing
			return (False, "Email already taken")
		cur.execute("INSERT INTO Auth(username) values ({})".format(user_info["username"]))
		cur.execute("INSERT INTO Auth(password_salted) values ({})".format(password_salted))
		cur = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1
		cur.execute("INSERT INTO User_info(email) values ({})".format(user_info["email"]))
		cur.execute("INSERT INTO User_info(join_date) values ({})".format(time.strftime("%Y/%m/%d")))
		return True
	except:
		return (False, "Unable to establish database connection")

def sign_up_user_details_optinal(user_info):
	try:
		cur = database_conn("User_info.db", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1
		for elem in user_info:
			cur.execute("INSERT INTO User_info({}) values ({})".format(str(elem), str(user_info[elem])))
		return True
	except:
		return (False, "Unable to establish database connection")

##########################
###### Grab details ######
##########################

def get_user_details(user_info):
	try: 
		cur = database_conn("Auth.db", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		cur.execute("SELECT * from Auth WHERE username=\"{}\"".format(User_info["username"]))
		indata = cur.fetchall()
		userid = indata[0]
		cur = database_conn("User_info.db", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1
		cur.execute(" SELECT * FROM information_schema.colums WHERE table_schema")
		indata1 = cur.fetchall
		cur.execute("SELECT * FROM User_info WHERE userid=\"{}\"".format(userid))
		indata2 = cur.fetchall()
		del data_dict["id"]
		for if_null in indata2:
			if if_null == "null"

		data_dict = dict(zip(indata1, indata2))
		return data_dict # we'll filter out the first key 
	except:
		return (False, "Unable to establish database connection")


#def shared_presentation(pres_uid, account_or_email):

