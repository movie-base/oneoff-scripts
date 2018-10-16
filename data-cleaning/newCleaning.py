import pandas as pd
import numpy as np
import requests
import re
import json

# add movie to mongodb
def createMovie(movie, count):
    endpoint = "http://45.63.27.74:8080/movies"
    headers = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjViYzEzOGE5MTdjOTViMDhiZjAyOWY3YSIsImlhdCI6MTUzOTU3OTc3MX0.GHtp4JdrVUDjOXh66cw7TUE6UCk3s6q9XXu4EfNJjZU"}
    try:
        requests.post(endpoint, data=movie, headers=headers)
        print(f' {count}. Added {movie["title"]}')
    except:
        print(f'### Failed to add {movie["title"]}')
        raise
    return

#makes it easier to differentiate between json objects when printing them
def printJson(data):
    print()
    for curr in data:
        print("----START OF JSON----")
        print(curr)
        print("----END OF JSON----")
    print()

# format the writers object properly
def formatWriters(writers):
    for x in range(len(writers)):
        writers[x] = re.sub(r'\(.*\)$', '', writers[x])
        writers[x] = re.sub(r'^\s', '', writers[x])
        writers[x] = re.sub(r'\s*$', '', writers[x])
    return writers

# format languages so there is no white spaces at the start of the string
def formatLanguage(language):
    for x in range(len(language)):
        language[x] = re.sub(r'^\s', '', language[x])
    return language

# format actos so there is no white spaces at the start of the string
def formatActors(actors):
    for x in range(len(actors)):
        actors[x] = re.sub(r'^\s', '', actors[x])
    return actors

# format genres so there is no white space at the start of the string
def formatGenres(genres):
    for x in range(len(genres)):
        genres[x] = re.sub(r'^\s', '', genres[x])
    return genres

# checking to see if there is a rotten tomatoe rating and setting Attribute
# if there is rotten tomatoe rating then just set it to N/A
def creatingRottenTomatoes(newJson, data):
    newJson['rottenTomatoesRating'] = None
    for x in range(len(data['Ratings'])):
        if(data['Ratings'][x]['Source'] == "Rotten Tomatoes"):
            rtRating = re.sub(r'\%$', '', data['Ratings'][x]['Value'])
            newJson['rottenTomatoesRating'] = None if rtRating == 'N/A' else float(rtRating)
    return newJson

def getYearTitle():
    # list used to store the title and year from the kaggle dataset
    allTitleYear = list ()
    # open json
    df = pd.read_csv(open("MovieGenre.csv",encoding="utf8",errors='replace'), delimiter=",")
    df = df.head(10)
    # iterate over df
    for i, row in df.iterrows():
        # make an array of size 2 and store title in index 0 and year in index 1
        currTitleYear = [None] * 2
        currTitleYear[0] = re.sub(r'\s*\(\d\d\d\d\)$','', row['Title'])
        try:
            currTitleYear[1] = re.search(r'\(\d\d\d\d\)$', row['Title']).group(0)[1:5]
        except:
            currTitleYear[1] = None
        # append the array
        allTitleYear.append(currTitleYear)
    return allTitleYear

def createJsonList(allTitleYear):
    # list used to store json objects generated
    jsonObjects = list ()
    count = 1
    for curr in allTitleYear:
        # make new json object
        newJson = {}
        # construct url and send request for json using the title and year from the kaggle dataset
        if(curr[1] != None):
            url = "https://www.omdbapi.com/?i=tt3896198&apikey=e7cda7bd&t=\"" + curr[0] + "\"" + "&y=\"" + curr[1] + "\""
        else:
            url = "https://www.omdbapi.com/?i=tt3896198&apikey=e7cda7bd&t=\"" + curr[0]
        data = requests.get(url).json()
        # checks if data returned is valid
        if("Response" in data.keys() and data["Response"] == "False"):
            print(f' {count}. Removed {data["Title"]}')
            continue
        # add relevant data to json and append to list of json objects
        if('imdbID' not in data.keys()):
            continue

        newJson['title'] = data['Title']

        if('Year' in data.keys()):
            newJson['year'] = None if data['Year'] == 'N/A' else data['Year']
        else:
            newJson['year'] = None

        if('Released' in data.keys()):
            newJson['released'] = None if data['Released'] == 'N/A' else data['Released']
        else:
            newJson['released'] = None

        if('Runtime' in data.keys()):
            newJson['runtime'] = None if data['Runtime'] == 'N/A' else data['Runtime']
        else:
            newJson['runtime'] = None

        if('Genre' in data.keys()):
            newJson['genres'] = None if data['Genre'] == 'N/A' else formatGenres(data['Genre'].split(','))
        else:
            newJson['genres'] = []

        if('Director' in data.keys()):
            newJson['directors'] = None if data['Director'] == 'N/A' else data['Director'].split(',')
        else:
            newJson['directors'] = []

        if('Writer' in data.keys()):
            newJson['writers'] = None if data['Writer'] == 'N/A' else formatWriters(data['Writer'].split(','))
        else:
            newJson['writers'] = []

        if('Actors' in data.keys()):
            newJson['actors'] = None if data['Actors'] == 'N/A' else formatActors(data['Actors'].split(','))
        else:
            newJson['actors'] = []

        if('Plot' in data.keys()):
            newJson['plot'] = None if data['Plot'] == 'N/A' else data['Plot']
        else:
            newJson['plot'] = None

        if('Language' in data.keys()):
            newJson['languages'] = None if data['Language'] == 'N/A' else formatLanguage(data['Language'].split(','))
        else:
            newJson['languages'] = []

        if('Country' in data.keys()):
            newJson['country'] = None if data['Country'] == 'N/A' else data['Country']
        else:
            newJson['country'] = None

        if('Poster' in data.keys()):
            newJson['poster'] = None if data['Poster'] == 'N/A' else data['Poster']
        else:
            newJson['poster'] = None

        if('Ratings' in data.keys()):
            newJson = creatingRottenTomatoes(newJson, data)
        else:
            newJson['rottenTomatoesRating'] = None

        if('Metascore' in data.keys()):
            newJson['metascore'] = None if data['Metascore'] == 'N/A' else float(data['Metascore'])
        else:
            newJson['metascore'] = None

        if('imdbRating' in data.keys()):
            newJson['imdbRating'] = None if data['imdbRating'] == 'N/A' else float(data['imdbRating'])
        else:
            newJson['imdbRating'] = None

        if('imdbVotes' in data.keys()):
            newJson['imdbVotes'] = None if data['imdbVotes'] == 'N/A' else int(re.sub(r',*', '', data['imdbVotes']))
        else:
            newJson['imdbVotes'] = None
        if('BoxOffice' in data.keys()):
            boxOffice = re.sub(r'\D', '', data['BoxOffice'])
            newJson['boxOffice'] = None if boxOffice == '' else float(boxOffice)
        else:
            newJson['boxOffice'] = None

        newJson['imdbId'] = data['imdbID']
        # createMovie(newJson, count)

        print(str(count) + ". " + newJson['title'] + " has been added to the list!")
        print(newJson)
        print()
        count = count + 1
    return


if __name__ == '__main__':
    allTitleYear = getYearTitle()
    createJsonList(allTitleYear)
