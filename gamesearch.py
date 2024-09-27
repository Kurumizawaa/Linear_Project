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