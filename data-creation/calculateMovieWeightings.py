# Weightings for each genre based on the findGenres.py script.
genreWeighting = {
	"Drama": 16,
	"Comedy": 11,
	"Romance": 5, "Action": 5, "Crime": 5, "Thriller": 5,
	"Documentary": 4, "Horror": 4, "Adventure": 4,
	"Mystery": 2, "Sci-Fi": 2, "Family": 2, "Biography": 2, "Fantasy": 2,
	"Animation": 2, "History": 2, "Short": 2, "Music": 2,
	"War": 1, "Western": 1, "Musical": 1, "Sport": 1, "Film-Noir": 1,
	"News": 1, "Adult": 1, "Reality-TV": 1, "Talk-Show": 1, "Game-Show": 1,
}

"""
	generateMoviesCsvWithWeightings reads an movies csv which contains id, genre, imdbRating
	and creates a new movies csv which contains the columns of the old movies csv but also
	a movie weighting. This weighting will be used to calculate the probability of a movie
	being watched.

	In the general case, weighting = imdbRating + genreWeighting[genreA] + genreWeighting[genreB] + genreWeighting[genreC]
"""
def generateMoviesCsvWithWeightings(oldCsvFilename, newCsvFilename):
	f = open(oldCsvFilename, "r")
	g = open(newCsvFilename, "w")

	header = f.readline().strip()
	g.write(header + ",weighting\n")
	for movieDetails in f:
		movieDetails = movieDetails.strip()
		id, genre, imdbRating = movieDetails.split(",")
		genreList = genre.split("*")

		weighting = 5 if imdbRating == "None" else float(imdbRating)
		for genre in genreList:
			if genre != "None":
				weighting += genreWeighting[genre]

		g.write(movieDetails + "," + str(weighting) + "\n")

	f.close()
	g.close()


# oldCsvFilename = XXXXX
# newCsvFilename = XXXXX
generateMoviesCsvWithWeightings(oldCsvFilename, newCsvFilename)