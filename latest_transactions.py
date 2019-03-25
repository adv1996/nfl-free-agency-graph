import requests
from bs4 import BeautifulSoup
import csv
from textblob import TextBlob

url = "https://www.spotrac.com/nfl/transactions/"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ajax\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"show\"\r\n\r\n200\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"original-load\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'Postman-Token': "e36f3db0-46af-47d5-a133-8cdcdf3fa4d7"
    }

response = requests.request("POST", url, data=payload, headers=headers)
teams = {
  'BAL': 0,
  'DEN': 1,
  'NYG': 2,
  'CLE': 3,
  'WAS': 4,
  'JAC': 5,
  'DET': 6,
  'DAL': 7,
  'PIT': 8,
  'OAK': 9,
  'KC': 10,
  'NYJ': 11,
  'PHI': 12,
  'HOU': 13,
  'LAR': 14,
  'GB': 15,
  'TB': 16,
  'CHI': 17,
  'SEA': 18,
  'NE': 19,
  'ARI': 20,
  'CAR': 21,
  'MIN': 22,
  'SF': 23,
  'ATL': 24,
  'TEN': 25,
  'IND': 26,
  'MIA': 27,
  'LAC': 28,
  'BUF': 29,
  'NO': 30,
  'CIN': 31,
}
def organize():
  soup = BeautifulSoup(response.text, 'lxml')
  players = soup.find_all('article')
  latest_transactions = {}
  for p in players:
    t = p.find('p')
    name = p.find_all('a')
    n = name[1].text.split(',')
    transInfoNLP = TextBlob(t.text)
    contract = []
    team = []
    playerAdd = False
    for tag in transInfoNLP.tags:
      if tag[0] == 'Signed':
        playerAdd = True
      if playerAdd:
        if tag[1] == 'CD':
          contract.append(tag[0])
        if tag[1] == 'NNP':
          team.append(tag[0])
    if playerAdd:
      apy = calculateAPY(contract)
      team = getTeam(team)
      latest_transactions[n[0]] = {
        'name': n[0],
        'apy': apy,
        'team': team,
      }
  return latest_transactions

def calculateAPY(contract):
  apy = 0
  if len(contract) > 1:
    if (len(contract) == 2):
      friendly_contract = contract[1]
      friendly_contract = friendly_contract.replace(',', '')
      friendly_contract = friendly_contract.replace('M', '')
      apy = float(friendly_contract) / int(contract[0])
    elif len(contract) == 3 and contract[2] == 'million':
      apy = (1000000 * float(contract[1])) / int(contract[0])
    else:
      apy = 0
  else:
    apy = 666666
  return apy

def getTeam(team):
  team_code = team[len(team) - 1]
  return teams[team_code]

players = organize()