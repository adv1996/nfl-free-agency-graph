import requests
from bs4 import BeautifulSoup
import csv
import time
# Getting Free Agency Data all From Over The Cap

# Get Headers from website_url
website_url = requests.get('https://overthecap.com/free-agency/').text
# Get Table Data From Post Request Tested in Postman, copied and pasted code snippet for python3 from postman
def setHeaders():
  website_url = requests.get('https://overthecap.com/free-agency/').text
  soup = BeautifulSoup(website_url, 'lxml')
  data = []
  table = soup.find('table', attrs={'class': 'controls-table'})
  table_head = table.find('thead')
  headers = table_head.find_all('th')
  thead = ['Year']
  for h in headers:
    if (h.text == '2018 Team'):
      thead.append('FTeam')
    elif (h.text == '2019 Team'):
      thead.append('NTeam')
    else:
      thead.append(h.text)
  data.append(thead)
  return data

def scrape(year, data):
  url = "https://overthecap.com/Includes/ajax.php"
  payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\nget_free_agents\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"year\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (year)

  headers = {
      'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
      'cache-control': "no-cache",
      'Postman-Token': "b6c1de02-ee2e-4344-8c11-9c59601a682a"
      }
  response = requests.request("POST", url, data=payload, headers=headers).text
  print('POSTED DATA WAITING 5 SECONDS')
  soup2 = BeautifulSoup(response, 'lxml')
  table_body = soup2.findAll('tr', attrs={'class': 'sortable'})
  for tb in table_body:
    item = tb.findAll('td')
    player = [year]
    for e in item:
      if '$' in e.text:
        salary = e.text[1::].replace(',', '')
        player.append(salary)
      else:
        player.append(e.text)
    data.append(player)
  print('Year: ' + str(year) + ' Number of Free Agents ' + str(len(data)))
  time.sleep(5)
  return data

def saveToCSV(data):
  filename = 'nflfaBULK.csv'
  with open(filename, 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(data)
  csvFile.close()
  print('Completed Web Scraping')

def buildDataFile():
  data = setHeaders()
  for year in range(2001, 2020):
    data = scrape(year, data)
  saveToCSV(data)

buildDataFile()