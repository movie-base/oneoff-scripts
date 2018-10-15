import json
import requests
import random
import string

EMAIL_EXTENSION = "@moviebase.local"
SYMBOLS = "!@#$%^&*"

# API_ENDPOINT = XXXXX


"""
	Returns an n-sized list of random unique emails.
"""
def generateNRandomEmails(n):
	
	ids = set()
	while len(ids) < n:
		ids.add(random.randint(1,999999))

	emails = []
	for id in ids:
		email = "test" + str(id) + EMAIL_EXTENSION
		emails.append(email)
	return emails

"""
	Returns an n-sized list of random passwords containing uppercase chars, lowercase chars,
	digits and symbols.
"""
def generateNRandomPasswords(n):
	passwords = []
	while len(passwords) < n:
	    passwordLength = random.randint(10,15)
	    passwordChars = []
	    while len(passwordChars) < passwordLength:    
		    passwordChars.append(random.choice(string.ascii_lowercase))
		    passwordChars.append(random.choice(string.ascii_uppercase))
		    passwordChars.append(str(random.randint(0,9)))
		    passwordChars.append(random.choice(SYMBOLS))
	    random.shuffle(passwordChars)
	    passwords.append(''.join(passwordChars))
	return passwords

"""
	Returns an n-sized list of dictionaries containing random unique emails and random passwords.
"""
def generateNRandomEmailsAndPasswords(n):
	emails = generateNRandomEmails(n)
	passwords = generateNRandomPasswords(n)

	result = []
	for i in xrange(n):
		d = {
			"email": emails[i],
			"password": passwords[i], 
		}
		result.append(d)
	return result

"""
	Returns an n users to the Moviebase database
"""
def addNUsersToDatabase(n):
	loginDetails = generateNRandomEmailsAndPasswords(n)
	for loginData in loginDetails:
		requests.post(API_ENDPOINT, data=loginData).json()


addNUsersToDatabase(500)