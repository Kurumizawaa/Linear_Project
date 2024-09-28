import numpy as np
from numpy.linalg import norm

import data

def searchbestmatch(playertype, query:dict):
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in data.gamelst:
        if game.playertype == playertype:
            gamegenre = np.array([game.genre[i] for i in game.genre])
            cosinesim = np.dot(searchquery,gamegenre)/(norm(searchquery)*norm(gamegenre))
            result[game] = cosinesim
    result = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
    result = dict(list(result.items()[:10]))

def searchbyname(name:str):
    for game in data.gamelst:
        if game.name.upper() == name.upper():
            gamename = game.name
            gameprice = game.price
            gametags = [key for key, value in game.tags.items() if value == 1]
            gamedesc = game.description
            return f"{gamename} | {gameprice} | {gametags} | {gamedesc}"
    return False

print(searchbyname('Black Myth: Wukong'))
