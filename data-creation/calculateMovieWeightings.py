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
	generateMoviesCsvWithWeightings reads a movies csv which contains id, genre, imdbRating
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

"""
	generateMoviesCsvWithProbabilities reads a movies csv which contains id, genre, imdbRating, weighting
	and creates a new movies csv which contains the columns of the old movies csv but also the probability,
	representing the likelihood of the movie being watched. To retrieve the probability, we must find the
	denominator by adding all the weightings together. The probability will be then calculated using the
	following formula:
		probability = weighting/denominator
"""
def generateMoviesCsvWithProbabilities(oldCsvFilename, newCsvFilename):
	f = open(oldCsvFilename, "r")
	g = open(newCsvFilename, "w")

	f.readline()	# Skip header

	# Calculate denominator by summing up the weightings
	weightingTotal = 0;
	for movieDetails in f:
		id, genre, imdbRating, weighting = movieDetails.strip().split(",")
		weightingTotal += float(weighting)


	# Write rows with probabilities to new file		
	f.seek(0)	# Restart file pointer

	header = f.readline().strip()
	g.write(header + ",probability\n")

	for movieDetails in f:
		movieDetails = movieDetails.strip()
		id, genre, imdbRating, weighting = movieDetails.split(",")
		probability = float(weighting) / weightingTotal
		g.write(movieDetails + "," + str(probability) + "\n")

	f.close()
	g.close()


# oldCsvFilename = XXXXX
# newCsvFilename = XXXXX
# generateMoviesCsvWithWeightings(oldCsvFilename, newCsvFilename)
generateMoviesCsvWithProbabilities(oldCsvFilename, newCsvFilename)