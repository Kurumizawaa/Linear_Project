import pandas as pd
from collections import Counter

class Game:
    def __init__(self, name, playertype, gametag, price, reviewtype, description = None, link = None, imgsrc = None):
        self.name = name
        self.playertype = playertype
        self.tags = {i : (1 if i in gametag else 0) for i in genre}
        self.price = price
        self.reviewtype = reviewtype
        self.description = None if not description else description
        self.link = None if not link else link
        self.imgsrc = None if not imgsrc else imgsrc

    def __str__(self) -> str:
        return f"{self.name}"
        
df = pd.read_csv('steam_cleaned.csv')
selected_df = df[['Name','Price','Review_type','Tags','Description']]
selected_df.dropna(inplace=True)

countdict = Counter()
for tags in selected_df['Tags']:
    for tag in tags.split(','):
        countdict[tag.strip()] += 1

countdict['Singleplayer'] = 0
countdict['Multiplayer'] = 0

sorttag = dict(countdict.most_common(30))
genrelst = []
for tag in sorttag.keys():
    if tag not in genrelst:
        genrelst.append(tag)

# print(genrelst)

genre = {i : 0 for i in genrelst}

gamelst = []
for index, game in selected_df.iterrows():

# Overwhelm pos | very pos | pos | mostly pos | mixed

    match game['Review_type']:
        case 'Overwhelmingly Positive':
            reviewtype = 4
        case 'Very Positive':
            reviewtype = 3
        case 'Positive':
            reviewtype = 2
        case 'Mostly Positive':
            reviewtype = 1
        case 'Mixed':
            reviewtype = 0
        case 'Mostly Negative':
            reviewtype = -1
        case 'Negative':
            reviewtype = -2
        case 'Very Negative':
            reviewtype = -3
        case 'Overwhelmingly Negative':
            reviewtype = -4
    gamelst.append(
        Game(
            game['Name'],
            'Single' if 'Singleplayer' in game['Tags'] else 'Multi', 
            game['Tags'], 
            game['Price'],
            reviewtype,
            game['Description']
            ))