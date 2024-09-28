import numpy as np
from numpy.linalg import norm

import data

def searchbestmatch(playertype, query:dict):
    """Input : playertype(Single | Multi), query(Tags)
       Operation : construct a vector of query then dot product by all game tags vector that pass playertype filter divide by size of query vector dot size of game tags vector
       Output : vector of games (1x10) sorted by cosine similarity score in descending order"""
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in data.gamelst:
        if game.playertype == playertype:
            gamegenre = np.array([game.tags[i] for i in game.tags])
            cosinesim = np.dot(searchquery,gamegenre)/(norm(searchquery)*norm(gamegenre))
            result[game] = cosinesim
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    sorted_result = [(game, cosinesim) for game, cosinesim in sorted_result]
    return sorted_result[:10]

def matrix_row_cosine_similarity(A, B):
    dot_product = np.matmul(A, B.T)
    A_norms = norm(A, axis=1).reshape(-1, 1)
    B_norms = norm(B, axis=1).reshape(1, -1)
    norm_product = A_norms * B_norms
    return dot_product / norm_product

def search_best_match_from_game(game_list):
    """Input : game_list(list of game object)
       Operation : construct matrix from row vector of tags of each input games and matrix from row vector of tags of all games then use each matrix row to perform cosine similarity then average all column to get 1D array then sort the array to get top 10 index then mapping each index to corresponding game object
       Output : vector of games (1x10)"""
    input_tags_matrix = np.array([[value for value in game.tags.values()] for game in game_list])
    all_game_tags_matrix = np.array([[value for value in game.tags.values()] for game in data.gamelst])
    res = matrix_row_cosine_similarity(input_tags_matrix, all_game_tags_matrix)
    res = np.mean(res, axis=0)
    ascending_index = np.argsort(res)
    descending_index = np.flip(ascending_index, axis=0)
    top10_best_match = [(data.gamelst[index], res[index]) for index in descending_index[:10]]
    return top10_best_match

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
        if game.tags[tagname] == 1:
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
inp = [1,1,0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,1]
i = 0
for genre in data.genrelst:
    genrequery[genre] = inp[i]
    i += 1

print(searchbestmatch('Multi',genrequery))
