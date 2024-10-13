# Website Host
from fastapi import FastAPI, HTTPException
import uvicorn

# Graph Plotting
import matplotlib.pyplot as plt
import seaborn as sns

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
                print('u fool')
                return
            elif passlen == user.passlen:
                if passlen < 16:
                    password.extend([0]*(16-passlen))
                passwordmat = np.array(password).reshape(4,4)
                passwordmat = np.matmul(encryptionkey, passwordmat)
                if passwordmat.all() == user.password.all():
                    currentuser = user
            return currentuser
    return "Incorrect username or password"

def register(username:str, password:str, passwordconfirm:str): #TODO: MOVE PASSWORDCONFIRM TO FRONTEND LATER
    global currentuser
    for user in userdata.userlst:
        if user.username == username:
            return "Username Taken"
    if password == passwordconfirm:
        password = [ord(char) for char in password]
        if len(password) > 16:
            print('no, less than 16 u imbecile')
            return
        else:
            passlen = len(password)
            if passlen < 16:
                password.extend([0]*(16-passlen))
            passwordmat = np.array(password).reshape(4,4)
            passwordmat = np.matmul(encryptionkey, passwordmat)
            newuser = userdata.User(username, passwordmat, passlen)
            userdata.userlst.append(newuser)
            currentuser = newuser
            return newuser
    else:
        print("Password Doesn't Match")
        return "Password Doesn't Match"
    
def logout():
    currentuser = None
    return currentuser
    
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

print("-" * 50)

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

res = search_best_match_from_game([game for game in gamedata.gamelst if game.name.upper() == "limbus company".upper()])
res = [game for game, _ in res]
sns.heatmap(covarience(res), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Covariance Matrix")
plt.show()

print(currentuser)
print(register('Nate Higgers','12345','12345'))
print(login('Nate Higgers', '12345'))
print(logout())

def euclidean_distance(coord1, coord2):
    return np.sqrt(np.sum((coord1 - coord2) ** 2))

def cosine_similarity(v1,v2):
    return np.dot(v1,v2)/(norm(v1)*norm(v2))

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