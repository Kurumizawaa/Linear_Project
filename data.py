import pandas as pd

class Game:
    def __init__(self, name, playertype, gamegenre, price, description = None, link = None, imgsrc = None):
        self.name = name
        self.playertype = playertype
        self.genre = {i : (1 if i in gamegenre else 0) for i in genre}
        self.price = price
        self.description = None if not description else description
        self.link = None if not link else link
        self.imgsrc = None if not imgsrc else imgsrc
        
genrelst = 'Open World, Story Rich, Action, Souls-like, Rhythm, Fighting, First-Person Shooter, Hack & Slash, Platformer, Third-Person Shooter, RPG, JRPG, Party-Based, Rogue-Like, Strategy, Turn-Based,Card & Board, City, Military, Real-Time Strategy, Tower Defense, Turn-Based Strategy, Adventure, Casual, Puzzle, Visual Novel, Simulation, Building, Dating, Farming, Hobby & Job, Life & Immersive, Sandbox & Physics, Space & Flight, Sports, Fishing & Hunting'
genre = {i : 0 for i in genrelst.split(', ')} 
gamelst = []

# p5r = Game(
#     'Persona 5 Royal',
#     'Single',
#     ['JPRG'],
#     20
# )
# print(p5r.genre)

df = pd.read_csv('steam_cleaned.csv')

selected_df = df[['Name','Price','Review_type','Tags','Description']]
selected_df.dropna(inplace=True)
print(selected_df)

# Seach by name
# Search by Genre (Single)
# Checkbox (Multiple)