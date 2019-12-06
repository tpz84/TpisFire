###############################################################################
##This is used for signing in##
import random 
prime = 110339
savedEmail = "email@email.com"
savedPassword = "IdkIdk"
salt1 = "tnfccaujnk"
salt2 = "niejmqfhep"

def createSalt():
    laps = 10
    salt = ""
    while laps > 0:
        ranNum = random.randint(97,122)
        ranLetter = chr(ranNum)
        salt = salt + ranLetter
        laps -= 1
    return salt

def hashThis(userCred):
    hashedTerm = ""
    toHash = salt1 + userCred + salt2
    stringLength = len(toHash)
    cutSpot = 0
    while stringLength > 0: 
        swapLetter = toHash[cutSpot]
        numberV = ord(swapLetter)
        hashedChar = numberV * prime
        hashedTerm = int(str(hashedTerm) + str(hashedChar))
        stringLength -= 1
        cutSpot -= 1
    return hashedTerm


def login(savedEmail, savedPassword):
    print("Welcome! Enter your email")
    userEmail = input()
    userEmail = userEmail.lower()
    print("What is your password?")
    userPassword = input()
    hashedSavedEmail = hashThis(savedEmail)
    hashedSavedPassword = hashThis(savedPassword)
    hashedUserEmail = hashThis(userEmail)
    hashedUserPassword = hashThis(userPassword)
    if hashedSavedEmail == hashedUserEmail:
        if hashedSavedPassword == hashedUserPassword:
            print("Welcome")
        else:
            print("Incorrect Password")
    else:
        print("Provided email is incorrect")
    


    
###############################################################################
#main
login(savedEmail, savedPassword)
