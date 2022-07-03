import sqlite3

'''
manages the users database for login
'''
class Users(object):
    def __init__(self, tablename="users", userId="userId", password="password", username="username", email="email", logo="logo"):
        self.__tablename = tablename
        self.__userId = userId
        self.__password = password
        self.__username = username
        self.__email = email
        self.__logo = logo

        self.file_name = 'users_db.db'
        conn = sqlite3.connect('users_db.db')
        print("Opened database successfully")

        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + self.__userId + " " + \
                    " INTEGER PRIMARY KEY AUTOINCREMENT ,"
        query_str += " " + self.__password + " TEXT    NOT NULL ,"
        query_str += " " + self.__username + " TEXT    NOT NULL ,"
        query_str += " " + self.__email + " TEXT    NOT NULL ,"
        query_str += " " + self.__logo + " TEXT   DEFAULT '1');"

        # conn.execute("Create table users")
        conn.execute(query_str)
        conn.commit()
        conn.close()

    def __str__(self):
        return "table  name is ", self.__tablename

    def get_table_name(self):
        return self.__tablename

    def insert_user(self, username, password, email):
        # insert new user into the database if not already exists
        print("inserting new user...")
        if not self.is_exist(username, email):  # check if user already exist
            conn = sqlite3.connect('users_db.db')  # before self.file_name
            insert_query = "INSERT INTO " + self.__tablename +\
                           " (" + self.__username + "," + self.__password + "," + self.__email + "," + self.__logo+ ") VALUES " \
                           "(" + "'" + username + "'" + "," + "'" + password + "'" + "," + "'" + email + "'" +\
                           "," + "'1'"+");"
            print(insert_query)
            conn.execute(insert_query)
            conn.commit()
            print("Record created successfully")
            return 1
            conn.close()
        else:
            return -1

    def get_phone(self, username):
        # get phone from username
        conn = sqlite3.connect('users_db.db')  # before self.file_name
        print(f"getting phone of {username}")
        str1 = f"select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[2] == username:
                conn.commit()
                conn.close()
                return row[3]
        cursor.close()
        conn.close()
        return "False"


#    def update_logo(self, username, logo_num):
#        # update the logo
#        conn = sqlite3.connect(self.file_name)
#        print("updating logo...")
#        str1 = f"UPDATE users SET logo={logo_num} WHERE username={username}"
#
#        if self.is_exist(username):
#            print("username exist")
#            conn.execute(str1)
#        else:
#            return "False"
#        conn.close()
#        return "True"


    def delete_user_by_id(self, userID):
        # delete user by id number
        conn = sqlite3.connect(self.file_name)
        str1 = f"DELETE FROM users WHERE userID LIKE {userID}"
        conn.execute(str1)
        conn.commit()
        conn.close()

    def update_password(self, phone, new_password):
        # update user password
        conn = sqlite3.connect(self.file_name)
        print("updating password...")
        str1 = f"UPDATE users SET password={new_password} WHERE email = {phone}"
        conn.execute(str1)
        conn.commit()
        conn.close()

    def find_username(self, username):
        # find if username in database
        conn = sqlite3.connect(self.file_name)
        str1 = ("SELECT rowid FROM components WHERE name = ?", username)

    def check_user_and_pass(self, username, password):
        # check if user and password as the same as those who've been given
        conn = sqlite3.connect(self.file_name)
        print("checking if user exists...")
        str1 = "select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[2] == username:
                if row[1] == password:
                    return True
        conn.commit()
        cursor.close()
        conn.close()
        return False

    def is_exist(self, username, email):
        # Checks if username or email already exist in database
        print("checking if username exist")
        conn = sqlite3.connect('users_db.db')
        str1 = f"select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[2] == username:
                return True
        for row in cursor:
            if row[3] == email:
                return True

        conn.commit()
        conn.close()
        return False

    def is_username_exist(self,myuser, username):
        # find is username is in database
        conn = sqlite3.connect('users_db.db')
        str1 = f"select * from users;"
        cursor = conn.execute(str1)
        for row in cursor:
            if row[2] == username and row[2] != myuser:
                return True

        conn.commit()
        conn.close()
        return False
