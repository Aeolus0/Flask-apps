
import time
import bcrypt
import psycopg2
##########################
###### Fundamentals ######
##########################

def database_conn(dbname, user, host, password):
	try:
		conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
		cur = conn.cursor
		return cur
	except:
		return (False, "Something went wrong in the database bits")

##########################
###### Sign in Stuff #####
##########################


def auth_user(user_info):
	try:
		cur = database_conn("Auth", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		cur.execute("SELECT * FROM AUTH WHERE username = {}".format(user_info["username"]))
		username_non_auth = cur.fetchall()
		# i don't think i need this since only one record will be returned password_hash_loc = 0
		if username_non_auth["password_salted"] == bcrypt.hash(user_info["password"], username_non_auth["password_salted"]):
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
		cur = database_conn("Auth", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		password_salted = bcrypt.hash(user_info["password"])
		if ((cur.execute("SELECT * FROM Auth(username) WHERE username = {}".format(user_info["username"]) != ""))):
			return (False, "Username already taken")
		if ((cur.execute("SELECT * FROM Auth(email) WHERE email {}".format(user_info["email"]) != ""))):
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
		cur = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
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
		cur = database_conn("Auth", "Auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
		# 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
		# Generated with echo "Auth_db_user" | openssl sha1
		cur.execute("SELECT * from Auth WHERE username=\"{}\"".format(User_info["username"]))
		indata = cur.fetchall()
		userid = indata[0]
		cur = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
		# 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
		# Generated with echo "User_info_db_user" | openssl sha1
		cur.execute("SELECT * FROM User_info WHERE userid=\"{}\"".format(userid))
		indata = cur.fetchall()
		return indata[1:] # no need to return the uniq user id as well 
	except:
		return (False, "Unable to establish database connection")


#def shared_presentation(pres_uid, account_or_email):

