import requests
from bs4 import BeautifulSoup
import csv
# Getting Free Agency Data all From Over The Cap

# Get Headers from website_url
website_url = requests.get('https://overthecap.com/free-agency/').text
# Get Table Data From Post Request Tested in Postman, copied and pasted code snippet for python3 from postman
url = "https://overthecap.com/Includes/ajax.php"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\nget_free_agents\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"year\"\r\n\r\n2019\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'Postman-Token': "b6c1de02-ee2e-4344-8c11-9c59601a682a"
    }

response = requests.request("POST", url, data=payload, headers=headers).text

soup = BeautifulSoup(website_url, 'lxml')
soup2 = BeautifulSoup(response, 'lxml')
def scrape():
  data = []
  table = soup.find('table', attrs={'class': 'controls-table'})
  table_head = table.find('thead')
  headers = table_head.find_all('th')
  thead = []
  for h in headers:
    thead.append(h.text)
  data.append(thead)
  table_body = soup2.findAll('tr', attrs={'class': 'sortable'})
  for tb in table_body:
    item = tb.findAll('td')
    player = []
    for e in item:
      if '$' in e.text:
        salary = e.text[1::].replace(',', '')
        player.append(salary)
      else:
        player.append(e.text)
    data.append(player)
  print('Total Players', len(data))
  saveToCSV(data)

def saveToCSV(data):
  filename = 'nflfa2019.csv'
  with open(filename, 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(data)
  csvFile.close()
  print('Completed Web Scraping')
scrape()