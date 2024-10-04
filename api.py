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

@app.get("/") # Recommend from search History
async def index():
    result = []
    result.extend(main.besthistorymatch('Multi',main.currentuser.getsearchavg()))
    result.extend(main.besthistorymatch('Single',main.currentuser.getsearchavg()))
    return result

@app.get('/currentuser') # get current user
async def currentuser():
    return main.currentuser
