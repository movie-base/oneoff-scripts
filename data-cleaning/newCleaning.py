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
    newJson['rottenTomatoesRating'] = "N/A"
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
    df = df.head(100)
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
            url = "https://www.omdbapi.com/?i=tt3896198&apikey=1e6a24c2&t=\"" + curr[0] + "\"" + "&y=\"" + curr[1] + "\""
        else:
            url = "https://www.omdbapi.com/?i=tt3896198&apikey=1e6a24c2&t=\"" + curr[0]
        data = requests.get(url).json()
        # checks if data returned is valid
        if("Response" in data.keys() and data["Response"] == "False"):
            continue
        # add relevant data to json and append to list of json objects
        newJson['title'] = data['Title']
        newJson['year'] = data['Year']
        newJson['released'] = data['Released']
        newJson['runtime'] = data['Runtime']
        newJson['genres'] = formatGenres(data['Genre'].split(','))
        newJson['directors'] = data['Director'].split(',')
        newJson['writers'] = formatWriters(data['Writer'].split(','))
        newJson['actors'] = formatActors(data['Actors'].split(','))
        newJson['plot'] = data['Plot']
        newJson['langauge'] = formatLanguage(data['Language'].split(','))
        newJson['country'] = data['Country']
        newJson['poster'] = data['Poster']
        newJson = creatingRottenTomatoes(newJson, data)
        newJson['metascore'] = None if data['Metascore'] == 'N/A' else float(data['Metascore'])
        newJson['imdbRating'] = None if data['imdbRating'] == 'N/A' else float(data['imdbRating'])
        newJson['imdbVotes'] = int(re.sub(r',*', '', data['imdbVotes']))
        newJson['imdbId'] = data['imdbID']
        boxOffice = re.sub(r'[\$,]', '', data['BoxOffice'])
        newJson['boxOffice'] = None if boxOffice == 'N/A' else float(boxOffice)
        # print(str(count) + ". " + newJson['title'] + " and the rating = " + str(newJson['rottenTomatoesRating']) + " has been added to the list!")
        createMovie(newJson, count)

        count = count + 1
    return


if __name__ == '__main__':
    allTitleYear = getYearTitle()
    createJsonList(allTitleYear)
