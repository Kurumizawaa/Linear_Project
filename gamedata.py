import pandas as pd
from collections import Counter

class Game:
    def __init__(self, name, playertype, gametag, price, reviewno, reviewtype, description = None):
        self.name = name
        self.playertype = playertype
        self.tags = {i : (1 if i in gametag else 0) for i in genre}
        self.price = price
        self.reviewno = reviewno
        self.reviewtype = reviewtype
        self.description = None if not description else description

    def __str__(self) -> str:
        return f"{self.name}"
    
selected_df = pd.read_csv('main_data.csv', index_col=0)

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
            game['Review_no'],
            reviewtype,
            game['Description']
            ))
    
mca_result = pd.read_csv('3000game_mca_10coordinates.csv', index_col=0)