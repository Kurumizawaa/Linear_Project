import pandas as pd
from collections import Counter

class Game:
    def __init__(self, name, playertype, gamegenre, price, description = None, link = None, imgsrc = None):
        self.name = name
        self.playertype = playertype
        self.genre = {i : (1 if i in gamegenre else 0) for i in genre}
        self.price = price
        self.description = None if not description else description
        self.link = None if not link else link
        self.imgsrc = None if not imgsrc else imgsrc
        
df = pd.read_csv('steam_cleaned.csv')
selected_df = df[['Name','Price','Review_type','Tags','Description']]
selected_df.dropna(inplace=True)

countdict = Counter()
for tags in selected_df['Tags']:
    for tag in tags.split(','):
        countdict[tag.strip()] += 1
sorttag = dict(countdict.most_common(30))
genrelst = []
for tag in sorttag.keys():
    if tag not in genrelst:
        genrelst.append(tag)

genre = {i : 0 for i in genrelst} 
gamelst = []

print(sorttag)
print(genre)


# Seach by name
# Search by Genre (Single)
# Checkbox (Multiple)
