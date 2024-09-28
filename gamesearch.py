import numpy as np
from numpy.linalg import norm

import data

def searchbestmatch(playertype, query:dict):
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in data.gamelst:
        if game.playertype == playertype:
            gamegenre = np.array([game.tags[i] for i in game.tags])
            cosinesim = np.dot(searchquery,gamegenre)/(norm(searchquery)*norm(gamegenre))
            result[game] = cosinesim
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    sorted_result = [game for game, cosinesim in sorted_result]
    return sorted_result[:11]

def searchbyname(name:str):
    for game in data.gamelst:
        if game.name.upper() == name.upper():
            gamename = game.name
            gameprice = game.price
            player = game.playertype
            gametags = [key for key, value in game.tags.items() if value == 1]
            gamedesc = game.description
            return f"{gamename} | {gameprice} | {player} | {gametags} | {gamedesc}"
    return False

def searchbytags(tagname:str):
    result = []
    for game in data.gamelst:
        if tagname in game.tags:
            gamename = game.name
            gameprice = game.price
            player = game.playertype
            gametags = [key for key, value in game.tags.items() if value == 1]
            gamedesc = game.description
            result.append(f"{gamename} | {gameprice} | {player} | {gametags} | {gamedesc}")
    return result if result is not None else False

print(searchbyname('Firelight Fantasy: Resistance'))

print('\n'.join(searchbytags('RPG')))

genrequery = {i : 0 for i in data.genrelst}

# Manual input
# for genre in data.genrelst:
#     genrequery[genre] = input(f'{genre} : ')

# Auto input : Targeted 'Black Myth: Wukong'
# inp = [1,1,0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,1]
# i = 0
# for genre in data.genrelst:
#     genrequery[genre] = inp[i]
#     i += 1

print(searchbestmatch('Multi',genrequery))
