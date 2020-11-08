import yaml
import json
import urllib.request
import datetime
import csv
import os.path

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),'config.cfg')
DATA_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.json')
cfg = yaml.load(open(CONFIG_FILE, 'r'), Loader=yaml.FullLoader)
PRIVAT_ID = cfg['privat']['id']
PRIVAT_TOKEN = cfg['privat']['token']
PRIVAT_ACCOUNT = cfg['privat']['account']

url = 'https://acp.privatbank.ua/api/statements/balance/final?acc='+PRIVAT_ACCOUNT
headers = {
  'User-Agent' : 'Python3 baby',
  'Content-Type' : 'application/json;charset=utf8',
  'id' : PRIVAT_ID,
  'token' : PRIVAT_TOKEN }

req = urllib.request.Request(url, None, headers)
response = urllib.request.urlopen(req)
result = json.loads(response.read())
balance = result['balances'][0]["balanceOut"]

data = {}
data['balance'] = balance
data['day'] = datetime.date.today().strftime("%d/%m/%Y")
data['time'] = datetime.datetime.now().strftime("%H:%M")

with open(DATA_FILE, 'w') as outfile:
    json.dump(data, outfile)
