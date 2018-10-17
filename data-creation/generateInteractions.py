import json
import random
import requests

INTERACTIONS_API_ENDPOINT = "http://45.63.27.74:8080/interactions"
USERS_API_ENDPOINT = "http://45.63.27.74:8080/users"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjViYzEzOGE5MTdjOTViMDhiZjAyOWY3YSIsImlhdCI6MTUzOTU3NDM3OX0.ZjUTTbQe5BMCRFK14nkRi13ZCA4zyhQ7bIIOs2DMfd4"

MOVIES_CSV = "weighted-movies-2.csv"

"""
	postInteraction posts data to the INTERACTIONS_API_ENDPOINT.
"""
def postInteraction(data):
	print requests.post(
		INTERACTIONS_API_ENDPOINT,
		headers = {"Authorization":"Bearer " + TOKEN},
		data = data,
	).json()

"""
	getAllUsers returns a list of all users stored on the server.
"""
def getAllUsers():
	result = []
	for i in xrange(1, 7):
		users = requests.get(
			USERS_API_ENDPOINT + "?limit=100&page=" + str(i),
			headers = {"Authorization":"Bearer " + TOKEN},
		).json()
		result.extend(users)
	return result

"""
	getAllUserIds returns a list of all users stored on the server.
"""
def getAllUserIds():
	users = getAllUsers()
	return [
		user['id']
		for user in users
	]

"""
	getHashValue returns a value between 0 and 4000 based on the userId.
"""
def getHashValue(userId):
	return abs(hash(userId)) % 4000

"""
	isValueInCircularBounds returns a boolean whether the value is within the specified
	bounds. This function also takes into the case where the lowerBound is greater than
	the upperBound.
"""
def isValueInCircularBounds(value, lowerBound, upperBound):
	result = False
	if lowerBound < upperBound:
		if lowerBound <= value and value <= upperBound:
			result = True
	else:
		if value <= upperBound or lowerBound <= value:
			result = True
	return result

"""
	didUserWatchMovie returns a boolean indicating if a user has watched a movie. To
	retrieve this value, we hash the userId and obtain a 'random' integer value
	between 0 and 4000. We then scale the movie probability, such that it is within the
	ranges of 0 and 4000. We then generate a range (lowerBound, upperBound).
		* The lowerBound is another 'random' hashed value between 0 and 4000.
		* The upperBound = lowerBound + probability

	If the userId is between the ranges, then the user declare that the user has watched
	the movie.
"""
def didUserWatchMovie(userId, movieProbability, movieId):
	# scaledProbability is guaranteed to be in the range of 1 to 4000, as:
	#   * min probability value = 3.99120009194e-06 (3.99)
	#   * max probability value = 7.47317810318e-05 (74.7)
	scaledProbability = movieProbability * 10**6
	
	h1 = getHashValue(userId)
	lowerBound = getHashValue(movieId)
	upperBound = (lowerBound + scaledProbability) % 4000

	return isValueInCircularBounds(h1, lowerBound, upperBound)

"""
	didUserLikeMovie returns a boolean indicating if a user has liked a movie. To
	retrieve this value, we hash the (userId + movieId) and obtain a 'random' 
	integer value between 0 and 4000. If the hashed value <= 2800, then we declare
	that the user has liked the film.
"""
def didUserLikeMovie(userId, movieId):
	h1 = getHashValue(userId + movieId)
	result = False
	if h1 <= (0.7 * 4000):
		result = True
	return result

"""
	doesUserWantToWatchMovie returns a boolean indicating if a user wants to watch
	a movie. To retrieve this value, we hash the userId and movieId to obtain a
	'random' integer value between 0 and 4000. If the hash value <= 2, then we declare
	that the user wants to watch the film.
"""
def doesUserWantToWatchMovie(userId, movieId):
	h1 = (getHashValue(userId) + getHashValue(movieId)) % 4000
	result = False
	if h1 <= (0.0005 * 4000):
		result = True
	return result	

"""
	generateMovieInteractionsForUser returns a list of interactions for a user, where each
	interaction is defined as:
		[movieId, hasWatched, hasLiked, wantToWatch]

	Using a MOVIES_CSV, the function goes through each movie in the file. It then runs the
	following functions, generating an interaction list.
		* didUserWatchMovie
		* didUserLikeMovie (if user watched movie)
		* doesUserWantToWatchMovie (if user did not watch movie)

	If any of the functions returns a true, the interaction is added to the interactions
	list, which is eventually returned.
"""
def generateMovieInteractionsForUser(userId):
	interactions = []
	f = open(MOVIES_CSV, "r")
	f.readline()	# Skip header
	for movieDetails in f:
		movieId, genres, imdbRating, weighting, probability = movieDetails.strip().split(",")
		probability = float(probability)
		hasWatched = didUserWatchMovie(userId, probability, movieId)
		hasLiked = False
		wantToWatch = False
		if hasWatched:
			hasLiked = didUserLikeMovie(userId, movieId)
		else:
			wantToWatch = doesUserWantToWatchMovie(userId, movieId)
		if hasWatched or hasLiked or wantToWatch:
			interactions.append([movieId, hasWatched, hasLiked, wantToWatch])

	f.close()
	return interactions

"""
	generateAndPostMovieInteractionsForAllUsers runs generateMovieInteractionsForUser and 
	obtains a list of interactions for each user. It then posts each interaction to the 
	INTERACTIONS_API_ENDPOINT.

	However, an extra requirement is that we want each movie to be watched at least twice.
	For the remaining movies that have been watched less than twice, we iterate through a
	user list until we find 2 users that have not watched the film. Those users are then 
	declared to have watched the film and a corresponding interaction is posted.
"""
def generateAndPostMovieInteractionsForAllUsers():
	movieToUserMap = {}	# Maps a movieId to a set of users that have watched the movie.

	f = open(MOVIES_CSV, "r")
	f.readline()	# Skip header
	for movieDetails in f:
		movieId, genres, imdbRating, weighting, probability = movieDetails.strip().split(",")
		movieToUserMap[movieId] = set()
	f.close()

	userIds = getAllUserIds()
	for i in xrange(len(userIds)):
		print "user " + str(i) + "'s interactions are being added."
		userId = userIds[i]
		interactions = generateMovieInteractionsForUser(userId)
		for interaction in interactions:
			movieId, hasWatched, hasLiked, wantToWatch = interaction
			data = {
				"user": userId,
				"movie": movieId,
				"hasLiked": "true" if hasLiked else "false",
				"hasWatched": "true" if hasWatched else "false",
				"wantToWatch": "true" if wantToWatch else "false",
			}
			postInteraction(data)
			if hasWatched:
				movieToUserMap[movieId].add(userId)
		print "user " + str(i) + "'s " + str(len(interactions)) +" interactions have been added."

	i = 0
	for movieId in movieToUserMap:
		numAdded = 0
		while len(movieToUserMap[movieId]) < 2:
			userId = userIds[i]
			if userId not in movieToUserMap[movieId]:
				movieToUserMap[movieId].add(userId)
				hasLiked = didUserLikeMovie(userId, movieId)
				data = {
					"user": userId,
					"movie": movieId,
					"hasLiked": "true" if hasLiked else "false",
					"hasWatched": "true",
					"wantToWatch": "false",
				}
				postInteraction(data)
				print "user " + userId + " has watched movie " + movieId

				numAdded += 1
			i = (i+1) % len(userIds)
		print "movie " + movieId + " has movies allocated to 2+ users (" + str(numAdded) + "/"+ str(len(movieToUserMap[movieId])) + " added)"

if __name__== "__main__":
	generateAndPostMovieInteractionsForAllUsers()
