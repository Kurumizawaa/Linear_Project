import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from nltk import edit_distance

app = FastAPI()

if __name__ == "__main__" :
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")

# ----------------------------
import main
import gamedata
import userdata
import schema
# ----------------------------

# http://127.0.0.1:8000/docs
# uvicorn api:app --reload
# python -m uvicorn api:app --reload

#----------------DON'T TOUCH------------------------#
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
#----------------DON'T TOUCH------------------------#

# @app.get("/") # Recommend from search History
# async def index():
#     result = main.searchuserhistory()
#     return result

@app.get('/currentuser') # get current user
async def currentuser():
    return main.currentuser

@app.post('/login') # log in
async def login(login: schema.Login):
    login = main.login(login.username, login.password)
    return login

@app.post('/signup') # sign up
async def signup(signup: schema.Signup):
    signup = main.signup(signup.username, signup.password)
    return signup

@app.get('/logout') # log out
async def logout():
    logout = main.logout()
    return logout

@app.get('/gettags') # get common tags
async def gettags():
    return gamedata.genre

@app.get('/getsteam') # get image source
async def getsteam(gamename: str):
    return main.getsteam(gamename)

@app.get('/searchbyname') # find best match from name
async def searchname(name: str):
    return main.searchbyname(name)

@app.get('/seachbestmatch') # find best match for query
async def seachbestmatch(tags: str, playertype: str):
    return main.websearch(tags, playertype)
# Test : 110101010000011001000001001011 | Must show Black Myth: Wukong

@app.get('/searchtag') # find best match for single tag
async def searchtag(tag: str, playertype: str):
    return main.websearchtag(tag, playertype)

@app.get('/besthistorymatch') # find best match from search history
async def besthistorymatch():
    return main.searchuserhistory()

@app.get('/get_game_name_list') # get game name list
async def get_game_name_list():
    return [game.name for game in gamedata.gamelst[:3000]]

@app.get('/mca_best_match') # find best match from mca
async def mca_best_match(game_name: str):
    return main.mca_best_match(game_name)
