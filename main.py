# Website Host
from fastapi import FastAPI, HTTPException
import uvicorn

# Vector/Matrix Stuff
import numpy as np
from numpy.linalg import norm

# for String comparison
from fuzzywuzzy import fuzz

# Database
import gamedata
import userdata

app = FastAPI()

currentuser = None
currentuser = userdata.penis
    
def login(username:str, password:str):
    for user in userdata.userlst:
        if user.username == username and user.password == password:
            currentuser = user
            return user
    return "Incorrect username or password"

def register(username:str, passsword:str, passwordconfirm:str):
    for user in userdata.userlst:
        if user.name == username:
            return "Username Taken"
    if passsword == passwordconfirm:
        newuser = userdata.User(username,passsword)
        userdata.userlst.append(newuser)
        return newuser
    else:
        return "Password Doesn't Match"
    
def logout():
    currentuser = None
    return
    
def searchbestmatch(playertype, query:dict):
    """Input : playertype(Single | Multi), query(Tags)
       Operation : construct a vector of query then dot product by all game tags vector that pass playertype filter divide by size of query vector dot size of game tags vector
       Output : vector of games (1x10) sorted by cosine similarity score in descending order"""
    if currentuser:
        currentuser.addhistory(query)
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in gamedata.gamelst:
        if game.playertype == playertype:
            gamegenre = np.array([game.tags[i] for i in game.tags])
            cosinesim = np.dot(searchquery,gamegenre)/(norm(searchquery)*norm(gamegenre))
            result[game] = cosinesim
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    sorted_result = [(game, cosinesim) for game, cosinesim in sorted_result]
    return sorted_result[:10]

def besthistorymatch(playertype, query:dict):
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in gamedata.gamelst:
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
    all_game_tags_matrix = np.array([[value for value in game.tags.values()] for game in gamedata.gamelst])
    res = matrix_row_cosine_similarity(input_tags_matrix, all_game_tags_matrix)
    res = np.mean(res, axis=0)
    ascending_index = np.argsort(res)
    descending_index = np.flip(ascending_index, axis=0)
    top10_best_match = [(gamedata.gamelst[index], res[index]) for index in descending_index[:10]]
    return top10_best_match

def searchbyname(query_name: str):
    result = {}
    for game in gamedata.gamelst:
        similarity = fuzz.partial_ratio(game.name.upper(), query_name.upper())
        result[game] = similarity
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    if currentuser and sorted_result[0][1] >= 80:
        currentuser.addhistory(sorted_result[0][0].tags)
    return [game for game, similarity in sorted_result[:10]]

    # ------------ For Debugging -------------------
    # top10_results = [(game, similarity) for game, similarity in sorted_result[:10]]
    # formatted_result = []
    # for game, similarity in top10_results:
    #     gamename = game.name
    #     gameprice = game.price
    #     player = game.playertype
    #     gametags = [key for key, value in game.tags.items() if value == 1]
    #     gamedesc = game.description
    #     formatted_result.append(f"{gamename} | {gameprice} | {player} | {gametags} | {gamedesc} | Similarity: {similarity}%") 
    # return formatted_result if formatted_result else "Not Found."

def searchbytags(tagname:str):
    result = []
    for game in gamedata.gamelst:
        if game.tags[tagname] == 1:
            gamename = game.name
            gameprice = game.price
            player = game.playertype
            gametags = [key for key, value in game.tags.items() if value == 1]
            gamedesc = game.description
            if currentuser:
                currentuser.addhistory(game.tags)
            # result.append(f"{gamename} | {gameprice} | {player} | {gametags} | {gamedesc}") # For debugging
            result.append(game)
    return result if result is not None else False

print('----------By Name---------------')

print(searchbyname('Firelight Fantasy: Resistance'))

print('--------------By Tags-------------------')

bytagsresult = [game.name for game in searchbytags('RPG')]
print('\n'.join(bytagsresult))
# print('\n'.join(searchbytags('RPG')))

genrequery = {i : 0 for i in gamedata.genrelst}

# Manual input
# for genre in gamedata.genrelst:
#     genrequery[genre] = input(f'{genre} : ')

# Auto input : Targeted 'Black Myth: Wukong'
inp = [1,1,0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,1]
i = 0
for genre in gamedata.genrelst:
    genrequery[genre] = inp[i]
    i += 1

print('-----------------By Multiple Tags ----------------')

print(searchbestmatch('Single',genrequery))

print('----------------By history-----------------')

print(besthistorymatch('Multi',currentuser.getsearchavg()))
print(besthistorymatch('Single',currentuser.getsearchavg()))
