import sqlite3

'''
manages the users database for login
'''
class Users(object):
    def __init__(self, tablename="users", userId="userId", password="password", username="username"):
        self.__tablename = tablename
        self.__userId = userId
        self.__password = password
        self.__username = username

        self.file_name = 'users_for_slt.db'
        conn = sqlite3.connect('users_for_slt.db')
        print("Opened database successfully")

        query_str = "CREATE TABLE IF NOT EXISTS " + tablename + "(" + self.__userId + " " + \
                    " INTEGER PRIMARY KEY AUTOINCREMENT ,"
        query_str += " " + self.__password + " TEXT    NOT NULL ,"
        query_str += " " + self.__username + " TEXT    NOT NULL );"

        # conn.execute("Create table users")
        conn.execute(query_str)
        print("Table created successfully")
        conn.commit()
        conn.close()

    def __str__(self):
        return "table  name is ", self.__tablename

    def get_table_name(self):
        return self.__tablename

    def insert_user(self, username, password):
        # insert new user into the database
        print(username)
        print(password)
        conn = sqlite3.connect('users_for_slt.db')  # before self.file_name
        insert_query = "INSERT INTO " + self.__tablename +\
                       " (" + self.__username + "," + self.__password + ") VALUES " \
                       "(" + "'" + username + "'" + "," + "'" + password + "'" + ");"
        print(insert_query)
        conn.execute(insert_query)
        conn.commit()
        conn.close()
        print("Record created successfully")


    def select_user_by_id(self, userId):
        conn = sqlite3.connect(self.file_name)
        print("Opened database successfully")
        str1 = "select * from users;"

        """strsql = "SELECT userId, username, password  from " +  self.__tablename + " where " + self.__userId + "=" \
            + str(userId)
        """
        print(str1)
        cursor = conn.execute(str1)
        for row in cursor:
            print("userId = ", row[0])
            print("username = ", row[1])
            print("password = ", row[2])

        print("Operation done successfully")
        conn.close()

    def delete_user_by_id(self, userID):
        # delete user by id number
        conn = sqlite3.connect(self.file_name)
        print("Opened database successfully")
        str1 = f"DELETE FROM users WHERE userID LIKE {userID}"
        conn.execute(str1)
        conn.commit()
        conn.close()

    def update_password(self, id, new_password):
        # update user password
        conn = sqlite3.connect(self.file_name)
        print("Opened database successfully")
        str1 = f"UPDATE users SET password={new_password} WHERE userID = {id}"
        conn.execute(str1)
        conn.commit()
        conn.close()

    def find_username(self, username):
        # find if username in database
        conn = sqlite3.connect(self.file_name)
        str1 = ("SELECT rowid FROM components WHERE name = ?", username)

    def check_user_and_pass(self, username, password):
        conn = sqlite3.connect(self.file_name)
        print("Opened database successfully")
        str1 = f"SELECT * from {self.__tablename} WHERE username = {username} AND password = {password}')"

        conn.execute(str1)
        conn.commit()
        conn.close()

Users()