import numpy as np

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.searchhistory = []

    def getsearchavg(self):
        avgdict = {}
        dictnum = len(self.searchhistory)
        for search in self.searchhistory:
            for key, value in search.items():
                if key in avgdict:
                    avgdict[key] += value
                else:
                    avgdict[key] = value
        for key in avgdict:
            avgdict[key] /= dictnum
        return avgdict

userlst =[]
penis = User('Mr.Penis', '1234')
userlst.append(penis)