import yaml
import json
import urllib.request
import datetime
import csv
import os.path

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),'config.cfg')
DATA_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.json')
DATA_FILE2 = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.csv')
cfg = yaml.load(open(CONFIG_FILE, 'r'), Loader=yaml.FullLoader)
PRIVAT_ID = cfg['privat']['id']
PRIVAT_TOKEN = cfg['privat']['token']
PRIVAT_ACCOUNT = cfg['privat']['account']

url_balance = 'https://acp.privatbank.ua/api/statements/balance/interim?acc='+PRIVAT_ACCOUNT
url_transactions= 'https://acp.privatbank.ua/api/statements/transactions/interim?acc='+PRIVAT_ACCOUNT 
headers = {
  'Content-Type' : 'application/json;charset=utf8',
  'id' : PRIVAT_ID,
  'token' : PRIVAT_TOKEN }

reqb = urllib.request.Request(url_balance, None, headers)
responseb = urllib.request.urlopen(reqb)
resultb = json.loads(responseb.read())
balance = resultb['balances'][0]["balanceOut"]

data = {}
data['balance'] = balance
data['day'] = datetime.date.today().strftime("%d/%m/%Y")
data['time'] = datetime.datetime.now().strftime("%H:%M")
with open(DATA_FILE, 'w') as outfile:
    json.dump(data, outfile)

reqt = urllib.request.Request(url_transactions, None, headers)
responset = urllib.request.urlopen(reqt)
resultt = json.loads(responset.read())
transactions = resultt['transactions']
while resultt['exist_next_page']:
  url = 'https://acp.privatbank.ua/api/statements/transactions/interim?acc='+PRIVAT_ACCOUNT+'&followId='+resultt['next_page_id']
  reqt = urllib.request.Request(url, None, headers)
  responset = urllib.request.urlopen(reqt)
  resultt = json.loads(responset.read())
  transactions += resultt['transactions']

with open(DATA_FILE2, 'a') as out:
  csvout = csv.writer(out)
  for transaction in transactions:
    csvout.writerow([
        transaction['DAT_OD'].split(".")[0],
        transaction['DAT_OD'].split(".")[1],
        transaction['DAT_OD'].split(".")[2],
        transaction['TRANTYPE'],
        transaction['SUM'],
        transaction['OSND']])
