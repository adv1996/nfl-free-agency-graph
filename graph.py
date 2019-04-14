import json
import pandas
import latest_transactions
df = pandas.read_csv('nflfa2019.csv')

def takeIndex(elem):
  return elem['Index']
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
  
  nodes.sort(key=takeIndex)
  i = 0
  for index, row in df.iterrows():
    if row['Type'] == 'Signed':
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
          'status': 0,
          'value': row['Current APY'],
        })
        links.append({
          'source': playerIndex,
          'target': target,
          'status': 1,
          'value': row['Current APY'],
        })
      else:
        links.append({
          'source': source,
          'target': playerIndex,
          'status': 2,
          'value': row['Current APY'],
        })
      nodes.append(n)
      i += 1
    else:
      # if player is not officially signed that means OTC might not have the most
      # up to date information
      # for players that are unsiged we should look them up in latest_transactions.py
      playerIndex = i + 32
      source = teams[row['2018 Team']][1]
      n = {
        'Name': row['Player'],
        'Type': 'Player',
        'Pos': row['Pos.'],
        'Value': row['Current APY'],
        'Index': playerIndex,
        'Status': row['Type'],
        'CTeam': source,
      }
      # nodes must be sorted because they are linked based on position
      stitchPlayers = stitch(n)
      if len(stitchPlayers[0]) > 0:
        nodes.append(stitchPlayers[0])
        links = links + stitchPlayers[1]
        i += 1
      else:
        nodes.append(n)
        i += 1
        print('Player not signed', n['Name'])

  saveGraphtoCSV(nodes, links)

def saveGraphtoCSV(nodes, links):
  graph = {}
  graph['nodes'] = nodes
  graph['links'] = links
  with open('data.json', 'w') as outfile:
      json.dump(graph, outfile, sort_keys = True, indent = 2, ensure_ascii = False)
  outfile.close()
ltdict = latest_transactions.organize()

def stitch(pn):
  new_nodes = []
  new_links = []
  count = 1

  current = pn['Name']
  if current in ltdict:
    tp = ltdict[current]
    # changing teams
    n_node = {
      'Name': pn['Name'],
      'Type': 'Player',
      'Pos': pn['Pos'],
      'Value': tp['apy'],
      'Index': pn['Index'],
      'Status': 'Signed'
    }
    if (tp['team'] != pn['CTeam']):
      new_links.append({
        'source': pn['CTeam'],
        'target': pn['Index'],
        'status': 0,
        'value': tp['apy'],
      })
      new_links.append({
        'source': pn['Index'],
        'target': tp['team'],
        'status': 1,
        'value': tp['apy'],
      })
    else:
      new_links.append({
        'source': tp['team'],
        'target': pn['Index'],
        'status': 2,
        'value': tp['apy'],
      })
    count = count + 1
    return (n_node, new_links)
  return ([], [])
  

setTeamNodes()