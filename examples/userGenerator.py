import requests
import random
import json

hasLiked = {
    "hasLiked": "true",
    "hasWatched": "true",
    "wantToWatch": "false"
}

hasDisLiked = {
    "hasLiked": "false",
    "hasWatched": "true",
    "wantToWatch": "false"
}

wantToWatch = {
    "hasLiked": "false",
    "hasWatched": "false",
    "wantToWatch": "true"
}

states = [hasLiked, hasDisLiked, wantToWatch]

users = [{"email": "bruceeeee.wayne@gmail.com", "password": "$$Brucy12345"},
        {"email": "barry.allen@gmail.com", "password": "!!Barryaleen12345"},
        {"email": "clark.kent@gmail.com", "password": "##CLArky1234567"},
        {"email": "dick.grason@gmail.com", "password": "&Dicky1234"},
        {"email": "tony.stark@gmail.com", "password": "**Tonnyyy123456"}]


movies = ["5bc6d73215307d54331a42e3", "5bc6d72d15307d54331a42d1", "5bc6d6c315307d54331a415b","5bc6d63715307d54331a3f74",
        "5bc6c34415307d54331a2746", "5bc6c23c15307d54331a2612", "5bc6b2e515307d54331a15d3", "5bc6d21315307d54331a34ad",
        "5bc6c5da15307d54331a29a5", "5bc6a0ec15307d54331a0c87", "5bc69bbb15307d54331a019c", "5bc6911815307d543319e2b6",
        "5bc68b0215307d543319d246", "5bc688ad15307d543319c6ea", "5bc688a815307d543319c6d3", "5bc688a815307d543319c6d2",
        "5bc692c715307d543319e73b", "5bc6c21115307d54331a2575", "5bc6b6b715307d54331a1818", "5bc68ae515307d543319d1ba"]

interactions = []

def createUser(user):
    endpoint = "http://45.63.27.74:8080/users"
    try:
        createdUser = requests.post(endpoint, json=user).json()
        print(f'Added {user["email"]}')
    except:
        print(f'### Failed to add {user["email"]}')
        raise
    return createdUser

def postInteraction(interactions):
    endpoint = "http://45.63.27.74:8080/interactions"
    headers = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjViYzEzOGE5MTdjOTViMDhiZjAyOWY3YSIsImlhdCI6MTUzOTU3OTc3MX0.GHtp4JdrVUDjOXh66cw7TUE6UCk3s6q9XXu4EfNJjZU"}
    try:
        requests.post(endpoint, json=interactions, headers=headers)
        print(f' Added {interactions["user"]} and {interactions["movie"]}')
    except:
        print(f'### Failed to add {interactions["user"]}')
        raise
    return


for user in users:
    createdUser = createUser(user)
    for movie in movies:
        interaction = {}
        interaction["user"] = createdUser["user"]["id"]
        interaction["movie"] = movie
        state = random.choice(states)
        interaction = {**interaction, **state}
        interactions.append(interaction)
    for interaction in interactions:
        postInteraction(interaction)





#
