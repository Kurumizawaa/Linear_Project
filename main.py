# Website Host
from fastapi import FastAPI, HTTPException
import uvicorn

# Vector/Matrix Stuff
import numpy as np
np.set_printoptions(legacy='1.25')
from numpy.linalg import norm

# for String comparison
from fuzzywuzzy import fuzz

# Google Search
import requests
import re
from bs4 import BeautifulSoup

# Database
import gamedata
import userdata

app = FastAPI()

currentuser = None

encryptionkey = np.array([[1,0,0,0],
                          [2,1,0,0],
                          [3,3,1,0],
                          [4,6,4,1]])

def login(username:str, password:str):
    global currentuser
    for user in userdata.userlst:
        if user.username == username:
            password = [ord(char) for char in password]
            passlen = len(password)
            if passlen > 16:
                raise HTTPException(status_code=400, detail="Password must be less than 16 characters")
            elif passlen == user.passlen:
                if passlen < 16:
                    password.extend([0]*(16-passlen))
                passwordmat = np.array(password).reshape(4,4)
                passwordmat = np.matmul(encryptionkey, passwordmat)
                if np.array_equal(passwordmat, np.array(user.password).reshape(4,4)):
                    currentuser = user
                    return currentuser
                else:
                    raise HTTPException(status_code=400, detail="Incorrect password")
            raise HTTPException(status_code=400, detail="Incorrect password")
    raise HTTPException(status_code=400, detail="User not found")

def signup(username:str, password:str): #TODO: MOVE PASSWORDCONFIRM TO FRONTEND LATER
    for user in userdata.userlst:
        if user.username == username:
            raise HTTPException(status_code=400, detail="Username already exists")
    password = [ord(char) for char in password]
    if len(password) > 16:
        raise HTTPException(status_code=400, detail="Password must be less than 16 characters")
    else:
        passlen = len(password)
        if passlen < 16:
            password.extend([0]*(16-passlen))
        passwordmat = np.array(password).reshape(4,4)
        passwordmat = np.matmul(encryptionkey, passwordmat)
        newuser = userdata.User(username, passwordmat.tolist(), passlen)
        userdata.userlst.append(newuser)
        return newuser

def logout():
    global currentuser
    currentuser = None
    return currentuser
    
def searchby_playertype_genre(playertype, query:dict):
    """Input : playertype(Single | Multi), query(Tags)
       Operation : construct a vector of query then dot product by all game tags vector that 
                   pass playertype filter divide by size of query vector dot size of game tags vector
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
    sorted_result = [game for game, cosinesim in sorted_result]
    return sorted_result[:20]

def searchbestmatch(query:dict):
    if currentuser:
        currentuser.addhistory(query)
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in gamedata.gamelst:
        gamegenre = np.array([game.tags[i] for i in game.tags])
        cosinesim = np.dot(searchquery,gamegenre)/(norm(searchquery)*norm(gamegenre))
        result[game] = cosinesim
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    sorted_result = [game for game, cosinesim in sorted_result]
    return sorted_result[:20]

def websearch(tags:str, playertype:str):
    tags = [int(i) for i in tags]
    i = 0
    genrequery = {i : 0 for i in gamedata.genrelst}
    for genre in gamedata.genrelst:
        genrequery[genre] = tags[i]
        i += 1
    if playertype == 'single':
        return searchby_playertype_genre('Single', genrequery)
    elif playertype == 'multi':
        return searchby_playertype_genre('Multi', genrequery)
    else: # playertype == 'mixed'
        return searchbestmatch(genrequery)

def besthistorymatch(query:dict):
    result = {}
    searchquery = np.array([query[i] for i in query])
    for game in gamedata.gamelst:
        gamegenre = np.array([game.tags[i] for i in game.tags])
        cosinesim = np.dot(searchquery,gamegenre)/(norm(searchquery)*norm(gamegenre))
        result[game] = cosinesim
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    sorted_result = [game for game, cosinesim in sorted_result]
    return sorted_result[:10]

def searchuserhistory():
    if currentuser == None or currentuser.searchamount == 0:
        return []
    else:
        return besthistorymatch(currentuser.getsearchavg())
    
def matrix_row_cosine_similarity(A, B):
    dot_product = np.matmul(A, B.T)
    A_norms = norm(A, axis=1).reshape(-1, 1)
    B_norms = norm(B, axis=1).reshape(1, -1)
    norm_product = A_norms * B_norms
    return dot_product / norm_product

def search_best_match_from_game(game_list):
    """Input : game_list(list of game object)
       Operation : construct matrix from row vector of tags of each input games and matrix from row vector of tags of all games 
                   then use each matrix row to perform cosine similarity then average all column to get 1D array then sort the array 
                   to get top 10 index then mapping each index to corresponding game object
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
    return [game for game, similarity in sorted_result[:20]]

def searchbytags(tagname:str):
    result = []
    if currentuser:
        currentuser.searchhistory[tagname] += 1
        currentuser.searchamount += 1
    for game in gamedata.gamelst:
        if game.tags[tagname] == 1:
            result.append(game)
    result = sorted(result, key=lambda game: game.reviewno, reverse=True)
    return result[:20]
def searchby_playertype_tag(tagname:str, playertype):
    result = []
    if currentuser:
        currentuser.searchhistory[tagname] += 1
        currentuser.searchamount += 1
    for game in gamedata.gamelst:
        if game.tags[tagname] == 1 and game.playertype == playertype:
            result.append(game)
    result = sorted(result, key=lambda game: game.reviewno, reverse=True)
    return result[:20]
def websearchtag(tagname:str, playertype):
    if playertype == 'single':
        return searchby_playertype_tag(tagname, 'Single')
    elif playertype == 'multi':
        return searchby_playertype_tag(tagname, 'Multi')
    else: # playertype == 'mixed'
        return searchbytags(tagname)

def getsteamlink(query:str):
    searchquery = f'{query.replace(" ","+")}+on+Steam'
    x = requests.get(f'https://www.google.com/search?hl=en&tbm=isch&q={searchquery}')
    soup = BeautifulSoup(x.text, 'html.parser')
    steamlinks = soup.find_all('a')
    for steamlink in steamlinks:
        href = steamlink.get('href')
        if 'url?q=' in href and 'https://store.steampowered.com/app/' in href:
            return href[7:]

def getimglink(url:str):
    x = requests.get(url)
    soup = BeautifulSoup(x.text, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        if 'store_item_assets/steam/apps/' in image.get('src'):
            return image.get('src')
        
def getsteam(gamename:str):
    result = {'steamlink': '', 'imgsrc': ''}
    steamlink = getsteamlink(gamename)
    imgsrc = getimglink(steamlink) if steamlink else 'https://youtu.be/dQw4w9WgXcQ?si=6bKOlVvM5oFl5T1J'
    result['steamlink'] = steamlink if steamlink else 'https://youtu.be/dQw4w9WgXcQ?si=6bKOlVvM5oFl5T1J'
    result['imgsrc'] = imgsrc
    return result

def covarience(game_list):
    res = [[game.price, game.reviewtype] for game in game_list]
    print(res)
    game_matrix = np.array(res)
    row_mean = np.mean(game_matrix, axis=0)
    row_mean_matrix = np.tile(row_mean, (len(game_list), 1))
    print(row_mean_matrix)
    game_matrix_normalize = game_matrix - row_mean_matrix
    print(game_matrix_normalize)
    cov = (1/len(game_list)) * np.matmul(game_matrix_normalize.T,game_matrix_normalize)
    return cov

def euclidean_distance(coord1, coord2):
    return np.sqrt(np.sum((coord1 - coord2) ** 2))

def cosine_similarity(v1,v2):
    return np.dot(v1,v2)/(norm(v1)*norm(v2))

# ---------------- COVARIANCE TEST ---------------- 
# import matplotlib.pyplot as plt
# import seaborn as sns
# res = search_best_match_from_game([game for game in gamedata.gamelst if game.name.upper() == "limbus company".upper()])
# res = [game for game, _ in res]
# sns.heatmap(covarience(res), annot=True, cmap="coolwarm", fmt=".2f")
# plt.title("Covariance Matrix")
# plt.show()

index = gamedata.gamelst.index([game for game in gamedata.gamelst if game.name.upper() == "muse dash".upper()][0])
game_coords = gamedata.mca_result.loc[index].values

distances = {}
for other_index, other_coords in gamedata.mca_result.iterrows():
    if other_index != index:
        distances[other_index] = euclidean_distance(game_coords, other_coords.values)

sorted_distances = sorted(distances.items(), key=lambda x: x[1])

print(f"Games similar to {gamedata.gamelst[index].name}:")
for other_index, distance in sorted_distances[:10]:
    print(f"{gamedata.gamelst[other_index].name}: {distance}")
