import pymongo

"""
	downloadMovieData downloads id, genre and imdbRating from a MongoClient connectionUrl. It also
	takes in a csvFilename, which is used to store results.
"""
def downloadMovieData(connectionUrl, csvFilename):
	client = pymongo.MongoClient(connectionUrl)
	db = client.get_default_database().movies
	records = db.find(
		{},
		{'_id': 1, 'imdbRating': 1, 'genres': 1},
	)

	f = open(csvFilename, "w")
	f.write("id, genres, imdbRating\n")
	for record in records:
		id = str(record["_id"])
		genres = "-".join(record["genres"]) if record["genres"] else "None"
		imdbRating = str(record["imdbRating"])
		recordInfoString = ",".join([id, genres, imdbRating])

		f.write(recordInfoString + "\n")
	f.close()


# connectionUrl = XXXXX
# csvFilename = XXXXX
downloadMovieData(connectionUrl, csvFilename)