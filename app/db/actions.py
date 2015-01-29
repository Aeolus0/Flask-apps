import time
import os.path

import bcrypt
import psycopg2

##########################
###### Fundamentals ######
##########################


##########################
######    Schema    ######
##########################
#   CREATE TABLE Auth
# 	(id BIGINT PRIMARY KEY NOT NULL,
#	username              TEXT NOT NULL,
#	password_salted       TEXT NOT NULL,
#	email                 TEXT NOT NULL
#	);



#   CREATE TABLE User_info
#   (id BIGINT PRIMARY KEY NOT NULL,
#	name                  TEXT,
#	location              TEXT,
#	join_date             TEXT
#   );

def database_conn(dbname, user, host, password):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname, user, host, password))
        cur = conn.cursor()
        return cur
    except:
        return (False, "Something went wrong in the database connection")


##########################
###### Sign in Stuff #####
##########################


def auth_user(user_info):
    try:
        cur = database_conn("auth", "auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
        # 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
        # Generated with echo "Auth_db_user" | openssl sha1
        cur.execute("SELECT * FROM auth WHERE username={};".format(user_info["username"]))
        username_non_auth = cur.fetchall()
        password_hash_loc = 2
        record_loc = 0
        if username_non_auth[record_loc][password_hash_loc] == bcrypt.hashpw(user_info["password"], username_non_auth[record_loc][password_hash_loc]):
            return (True, "User authenticated")
        else:
            return (False, "Incorrect username or password")
    except:
        return (False, "Unable to establish database connection")


###########################
###### Sign Up Stuff ######
###########################


def sign_up_user(user_info):
    try:
        cur = database_conn("auth", "auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
        # 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
        # Generated with echo "Auth_db_user" | openssl sha1

        # check if the same username or password already exisits
        cur.execute("SELECT * FROM auth WHERE username={} OR email={};".format(user_info["username"], user_info["email"]))
        is_already_existing = cur.fetchall()
        if is_already_existing != []:
            uname_loc = 1
            email_loc = 3
            for elem in is_already_existing:
                if elem[uname_loc] == user_info["username"]:
                    return (False, "Username already taken")
                if elem[email_loc] == user_info["email"]:
                    return (False, "Email already taken")

        # store the username, salted password and email
        password_salted = bcrypt.hashpw(user_info["password"], bcrypt.gensalt())
        cur.execute("INSERT INTO auth(username, password_salted, email) values (\'{}\',\'{}\', \'{}\');".format(user_info["username"], password_salted, user_info["email"]))


        cur2 = database_conn("User_info", "User_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
        # 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
        # Generated with echo "User_info_db_user" | openssl sha1
        cur2.execute("INSERT INTO user_info(join_date) values (\'{}\');".format(time.strftime("%Y/%m/%d"))
        return (True, "User signed up")
    except:
        return (False, "Unable to establish database connection")



def sign_up_user_details_optinal(user_info):
    try:

        cur = database_conn("user_info", "user_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
        # 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
        # Generated with echo "User_info_db_user" | openssl sha1

        # TODO: Find a better way to do his than O(n)
        for elem in user_info:
            cur.execute("INSERT INTO user_info({}) values ({});".format(str(elem), str(user_info[elem])))
        return (True, "Additional values added")

    except:
        return (False, "Unable to establish database connection")


##########################
###### Grab details ######
##########################

def get_user_details(user_info):
    try:
        cur = database_conn("auth", "auth_db_user", "localhost", "4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4")
        # 4a9ae88667d0efcb4d596c5516b3fe3bf5a22ab4 is the SHA1 of "Auth_db_user"
        # Generated with echo "Auth_db_user" | openssl sha1

        cur.execute("SELECT * from auth WHERE username=\'{}\'".format(user_info["username"]))

        # Get the ID from the inner tuple
        indata = cur.fetchall()
        userid = indata[0][0]

        cur2 = database_conn("user_info", "user_info_db_user", "localhost", "8487997120e51bb4a83a5b4883f2b7daf80ac14a")
        # 8487997120e51bb4a83a5b4883f2b7daf80ac14a is the SHA1 of "User_info_db_user"
        # Generated with echo "User_info_db_user" | openssl sha1
        cur2.execute("SELECT * FROM user_info WHERE id=\'{}\'".format(userid))

        # Strip out the userid
        indata = cur.fetchall()
        outdata = indata[0][1:]

        return outdata
    except:
        return (False, "Unable to establish database connection")


# def shared_presentation(pres_uid, account_or_email):

