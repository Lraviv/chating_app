'''
This handles the registration and the login to the database
for each user and sends the encrypted data to the server
'''
#from client import Client

class Login(object):
    def __init__(self,client, creds):
        self.creds = creds
        (self.username, self.password) = self.creds
        print(self.creds)
        self.valid = True
        self.client = client
        print("in login")
        #TODO here send the creds to the client

    def is_valid(self):
        # send creds to server and receive whether the try is valid
        print("checking if ", self.creds, " in database...")
        # receive from server the credentials

        # check with the creds that the client provided

        # return true if creds match
        return self.valid



class Sign(object):
    def __init__(self, creds):
        self.creds = creds
        (self.username, self.password, self.email) = self.creds
        print("adding ", self.creds, " to database")

    def add_to_db(self):
        # add creds to database and send validation in email
        return True
