from pymongo import MongoClient
from bson.objectid import ObjectId
from SaltHashManager import saltHashManager


class mongoDBManager:

    _client = None
    _db = None

    # initialize
    def __init__ (self):
        self._client = MongoClient(
            'mongodb+srv://Vern:123qwer456@clustertest-ftjcv.gcp.mongodb.net/test?retryWrites=true&w=majority')
        print(self._client)
        self._db = self._client.get_database('TweetFeel')

    def login (self, email, password):
        user = self.checkPassword(email, password)
        if user is not None:
            print("Login successful!")
            return user
        else:
            print("Login failed!")
            return None

    def register (self, username, email, password):

        # protecting password
        SHM = saltHashManager()
        salt = SHM.createSalt()
        hashed = SHM.hashPassword(password, salt)

        u = {"username": username,
             "email": email,
             "salt": salt,
             "hash": hashed,
             "keywords": []
             }

        # insert to database
        try:
            db = self._db
            userCollection = db.Users
            userCollection.insert_one(u)
            print("Sign up successful!")
            return True

        except:
            print("Error signing up!")
            return False

    def checkEmailAvailability(self, email):
        db = self._db
        userCollection = db.Users
        user = userCollection.find_one({"email": email})
        if user == None:
            return True
        else:
            return False

    # def checkUsernameAvailability (self, username):
    #     db = self._db
    #     userCollection = db.Users
    #     user = userCollection.find_one({"username": username})
    #     if user == None:
    #         return False
    #     else:
    #         return True

    def changePassword (self, email, oldPassword, newPassword):
        db = self._db
        userCollection = db.Users

        user = self.checkPassword(email, oldPassword)
        if user is not None:
            print("user is valid")
            SHM = saltHashManager()
            salt = SHM.createSalt()
            hashed = SHM.hashPassword(newPassword,salt)

            update = {"salt": salt,
                      "hash": hashed}
            try:
                userCollection.update_one({"email": email}, {'$set' : update})
                print("Password updated!")
                return True
            except:
                print("Password failed to update!")
                return False

        else:
            print("wrong email or old password")
            return False

    def checkPassword (self, email, password):
        db = self._db
        userCollection = db.Users
        user = userCollection.find_one({"email": email})
        print(email)

        if user is not None:
            print("found user, checking password")
            SHM = saltHashManager()
            salt = user['salt']
            hashed = user['hash']

            checkPass = SHM.checkPass(password, hashed)
            if checkPass == True:
                return user
            else:
                return None
        else:
            print("user not found")
            return None

    def getKeywords(self, id):
        db = self._db
        userCollection = db.Users
        user = userCollection.find_one({"_id": ObjectId(id)})
        keywords = user['keywords']
        return keywords

    def getTweetDetails(self, keyword, id):
        db = self._db
        collection = db.Raw_Tweets
        tweetCollection = collection.find({"userid": ObjectId(id),
                                               "keyword": keyword})

        return tweetCollection


    def deleteOldTweetsDetails (self, keyword, id):
        db = self._db
        collection = db.Raw_Tweets
        try:
            tweetCollection = collection.delete_many({"userid": ObjectId(id),
                                           "keyword": keyword})
            return True
        except:
            print("delete unsuccessful!")
            return False


    def updateUserKeywords (self, newKeywords, id):
        db = self._db
        userCollection = db.Users
        user = userCollection.find_one({"_id": ObjectId(id)})
        oldKeywords= user['keywords']
        delKeywords = []

        for key in oldKeywords:
            if key not in newKeywords:
                delKeywords.append(key)
                print(key)

        for delKey in delKeywords:
            self.deleteOldTweetsDetails(delKey, id)

        update = {"keywords" : newKeywords}

        try:
            userCollection.update_one({"_id": ObjectId(id)}, {'$set': update})
            return True
        except:
            return False