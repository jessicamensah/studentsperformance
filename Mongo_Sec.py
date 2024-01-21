
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client.StudentsPerformance
collection = database.StudentSample

class MongoDBConnection:
    def __init__(self, host, port, username, password):
        self.client = MongoClient(host, port)
        self.db = self.client.StudentsPerformance
        self.db.authenticate(username, password)

    def close(self):
        self.client.close()

class UserAuthentication:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate_user(self, username, password): # identifying the users details to connect to MongoDB
        user = self.db_connection.db.users.find_one({"adminUser": username})
        if user and user["admin"] == password:
            return True
        return False

if __name__ == "__main__":
    db_connection = MongoDBConnection("localhost", 27017, "adminUser", "adminPassword")
    user_auth = UserAuthentication(db_connection)

    if user_auth.authenticate_user("admin", "admin"): # if the correct credentials are added
        print("User authenticated successfully.")

    else:
        print("Authentication failed.")
    
    db_connection.close()
