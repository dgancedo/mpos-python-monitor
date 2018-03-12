import requests
import json
import sys

def getmposapi(url,key,userid,action):
    response = requests.get(url + "?page=api&action=" + action + "&api_key=" + key + "&id=" + userid)
    data = json.loads(response.content)
    return data

key = "yourapikey"
userid = "youruserid"
url= "https://vrm.n3rd3d.com/index.php"

shownonmonitored = 0 #set to 1 if you want to show workers set as non monitored
colors = 0 #set to 1 if you want colored output

if colors == 1:
    red = '\x1b[1;31m'
    green = '\x1b[1;32m'
    yellow = '\x1b[1;33m'
    normal = '\x1b[0m'
    blue = '\x1b[1;34m'
else:
    red = ""
    green = ""
    yellow = ""
    normal = ""
    blue = ""


data = getmposapi(url,key,userid,"getuserbalance")
confirmedbalance = data['getuserbalance']['data']['confirmed'][:6]
unconfirmedbalance = data['getuserbalance']['data']['unconfirmed'][:6]
orphanedbalance = data['getuserbalance']['data']['orphaned'][:6]

sys.stdout.write("Account balance: Confirmed: " + green + confirmedbalance + normal + "\tUnconfirmed: " + yellow + unconfirmedbalance + normal + "\tOrphaned: " + red + orphanedbalance + normal + "\n\n")

print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Workers Status -=-=-=-=-=-=-=-=-=-=-=-=-=-=-") 
data = getmposapi(url,key,userid,"getuserworkers")
for worker in data['getuserworkers']['data']:
    if ((worker['monitor'] == 1) or (shownonmonitored == 1)):
        workername = worker['username'].split('.')[1]
        if worker['hashrate'] == 0: 
            color = red 
        else: 
            color = green
        sys.stdout.write("Worker: "+ color + workername + normal+ "\tHashrate: " + str(worker['hashrate'])[:12] + "\tShares: " + str(worker['shares'])[:6] + "\tdifficulty: " + str(worker['difficulty'])[:6] + "\n")
