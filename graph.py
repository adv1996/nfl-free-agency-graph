import pandas
import json
df = pandas.read_csv('nflfa2019.csv')

def setTeamNodes():
  teams = {
    'Ravens': ('BAL', 0),
    'Broncos': ('DEN', 1),
    'Giants': ('NYG', 2),
    'Browns': ('CLE', 3),
    'Redskins': ('WAS', 4),
    'Jaguars': ('JAC', 5),
    'Lions': ('DET', 6),
    'Cowboys': ('DAL', 7),
    'Steelers': ('PIT', 8),
    'Raiders': ('OAK', 9),
    'Chiefs': ('KC', 10),
    'Jets': ('NYJ', 11),
    'Eagles': ('PHI', 12),
    'Texans': ('HOU', 13),
    'Rams': ('LA', 14),
    'Packers': ('GB', 15),
    'Buccaneers': ('TB', 16),
    'Bears': ('CHI', 17),
    'Seahawks': ('SEA', 18),
    'Patriots': ('NE', 19),
    'Cardinals': ('ARI', 20),
    'Panthers': ('CAR', 21),
    'Vikings': ('MIN', 22),
    '49ers': ('SF', 23),
    'Falcons': ('ATL', 24),
    'Titans': ('TEN', 25),
    'Colts': ('IND', 26),
    'Dolphins': ('MIA', 27),
    'Chargers': ('LAC', 28),
    'Bills': ('BUF', 29),
    'Saints': ('NO', 30),
    'Bengals': ('CIN', 31),
  }
  nodes = []
  links = []
  # add team nodes
  for key, value in teams.items():
    nodes.append({
      'Name': value[0],
      'Type': 'Team',
      'Index': value[1]
    })
  
  is_signed = df['Type']=='Signed'
  fdf = df[is_signed]
  print(fdf.shape)
  print(df.shape)
  i = 0
  for index, row in fdf.iterrows():
    playerIndex = i + 32
    n = {
      'Name': row['Player'],
      'Type': 'Player',
      'Pos': row['Pos.'],
      'Value': row['Current APY'],
      'Index': playerIndex,
      'Status': row['Type']
    }
    # link = {source: 0, target: 5}
    source = teams[row['2018 Team']][1]
    target = teams[row['2019 Team']][1]
    if (row['2018 Team'] != row['2019 Team']):
      links.append({
        'source': source,
        'target': playerIndex,
        'status': 0
      })
      links.append({
        'source': playerIndex,
        'target': target,
        'status': 1
      })
    else:
      links.append({
        'source': source,
        'target': playerIndex,
        'status': 2
      })
    i += 1
    nodes.append(n)
  graph = {}
  graph['nodes'] = nodes
  graph['links'] = links
  with open('data.json', 'w') as outfile:
      json.dump(graph, outfile, sort_keys = True, indent = 2, ensure_ascii = False)
  outfile.close()


setTeamNodes()