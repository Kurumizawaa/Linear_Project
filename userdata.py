import numpy as np
import gamedata

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.searchhistory = {i : 0 for i in gamedata.genrelst}
        self.searchamount = 0
    
    def addhistory(self, tags:dict):
        for tag in tags:
            if tags[tag] == 1:
                self.searchhistory[tag] += 1
        self.searchamount += 1
        return self.searchhistory

    def getsearchavg(self):
        avgdict = self.searchhistory
        for key in avgdict:
            avgdict[key] /= self.searchamount
        return avgdict

userlst =[]
penis = User('Mr.Penis', '1234')
userlst.append(penis)
