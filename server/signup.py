from server.users import Users
"""
handles signup for each user: creates new user in database
"""
class sign(object):
    def __init__(self, user, password, email):
        self.username, self.password, self.email = user, password, email
        print(f"user {self.username} with {self.email} with password {self.password}")
        self.user = Users()

    def create_a_user(self):
        # creates a user from the given username and password
        print(self.username, self.password, self.email)
        success = self.user.insert_user(self.username, self.password, self.email)
        if success == 1:
            print(f"created {self.username} successfully")
            return True
        elif success == -1:
            print(f"can't create username because its already exists")
            return False

