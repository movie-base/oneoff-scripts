"""
	findGenres takes in a csv file of movies, and finds the genre frequency
	for each genre. It returns a list of genres, sorted in descending frequency.
	More specifically, the function returns:
	[
		('Drama', 15467), ('Comedy', 10394), ('Romance', 4995), ('Action', 4434), ('Crime', 4303),
		('Thriller', 4001), ('Documentary', 3391), ('Horror', 3363), ('Adventure', 3217), ('Mystery', 1992),
		('Sci-Fi', 1791), ('Family', 1770), ('Biography', 1678), ('Fantasy', 1670), ('Animation', 1387),
		('History', 1176), ('Short', 1155), ('Music', 1123), ('War', 973), ('Western', 765), ('Musical', 737),
		('Sport', 610), ('Film-Noir', 354), ('News', 73), ('Adult', 24), ('Reality-TV', 15), ('Talk-Show', 13),
		('Game-Show', 11),
	]
"""

def findGenres(csvFilename):
	moviesFile = open(csvFilename, "r")
	genreFrequency = {}

	moviesFile.readline()			# Skips header.
	for line in moviesFile:
		id, genres, rating = line.split(",")
		genreList = genres.split("*")
		for genre in genreList:
			if genre != "None":
				if genre not in genreFrequency:
					genreFrequency[genre] = 0
				genreFrequency[genre] += 1
	return sorted(genreFrequency.items(), key=lambda x:x[1], reverse=True)

# csvFilename = XXXXX
print findGenres(csvFilename)