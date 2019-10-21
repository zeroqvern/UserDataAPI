import bcrypt

class saltHashManager:

    # check password
    def checkPass (self, password, hashed):
        password = password.encode("utf-8")
        if bcrypt.checkpw(password, hashed):
            return True
        else:
            return False

    # generate random salt
    def createSalt (self):
        salt = bcrypt.gensalt()
        return salt
    # hash password
    def hashPassword(self, password, salt):
        password = password.encode("utf-8")
        hashed = bcrypt.hashpw(password, salt)
        return hashed




