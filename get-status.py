import requests
import json
import sys

def getmposapi(url,key,userid,action):
    response = requests.get(url + "?page=api&action=" + action + "&api_key=" + key + "&id=" + userid)
    data = json.loads(response.content)
    return data

def drawline(message):
    chars = len(message.translate(dict.fromkeys(range(32))))
    for i in range(1,int(chars)): 
        sys.stdout.write("-")
        i=i+1
    sys.stdout.write("\n")

key = sys.argv[1] # put your api key ir pass it as firsth argument.
userid = sys.argv[2] #put your user id or pass it as second argument.
url = "https://vrm.n3rd3d.com/index.php"

shownonmonitored = 1 #set to 1 if you want to show workers set as non monitored
showtotals = 1 #show total hashrate/sharerate after the workers
colors = 1 #set to 1 if you want colored output
html = 0 #se to 1 to get html output.

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
confirmedbalance = data['getuserbalance']['data']['confirmed'].split('.')[0] + "." + data['getuserbalance']['data']['confirmed'].split('.')[1][0:2]
unconfirmedbalance = data['getuserbalance']['data']['unconfirmed'].split('.')[0] + "." + data['getuserbalance']['data']['unconfirmed'].split('.')[1][0:2]
orphanedbalance = data['getuserbalance']['data']['orphaned'].split('.')[0] + "." + data['getuserbalance']['data']['orphaned'].split('.')[1][0:2]

if html == 1:
    message = ("<html><body>Account balance: Configrmed: <font color=\"green\">" + confirmedbalance + "</font>    Unconfirmed: <font color=\"yellow\">" \
    + unconfirmedbalance +"</font>    Orphaned: <font color=\"red\">" + orphanedbalance +"</font><br><hr><br>")
else:
    message = "Account balance: Confirmed: " + green + confirmedbalance + normal + "\tUnconfirmed: " + yellow + unconfirmedbalance + normal \
    + "\tOrphaned: " + red + orphanedbalance + normal + "\n\n"
    
sys.stdout.write(message)
if html != 1: drawline(message)

data = getmposapi(url,key,userid,"getuserworkers")
if html == 1:
    sys.stdout.write("<table>")
for worker in data['getuserworkers']['data']:
    if ((worker['monitor'] == 1) or (shownonmonitored == 1)):
        workername = worker['username'].split('.')[1]
        workerhashrate =  str(float("{0:.2f}".format(worker['hashrate'])))
        workersharerate = str(float("{0:.2f}".format(worker['shares'])))
        workerdificulty = str(float("{0:.2f}".format(worker['difficulty'])))
        if html == 1:
            if worker['hashrate'] == 0:
                color = "red"
            else:
                color = "green"
            sys.stdout.write("<tr><td>Worker:</td><td><font color=\"" + color + "\">" + workername + "</font></td><td>   </td><td>Hashrate:</td><td>" \
            + workerhashrate + "</font></td><td>   </td><td>Shares:</td><td>" + workersharerate + "</td><td>   </td><td>Difficulty:</td><td>" \
            + workerdificulty + "</td></tr>")
        else:
            if worker['hashrate'] == 0: 
                color = red 
                hashtab = "\t"
            else: 
                color = green
                hashtab = ""
            if len(workername) < 8:
                extratab = "\t"
            else:
                extratab = ""
            
            sys.stdout.write("Worker: " + color + workername + normal + extratab + "\tHashrate: " + workerhashrate + hashtab +"\tShares: " \
            + workersharerate + "\tDifficulty: " + workerdificulty + "\n")

if showtotals == 1:
    userhashrate = str(float("{0:.2f}".format(getmposapi(url,key,userid,"getuserhashrate")['getuserhashrate']['data'])))
    usersharerate = str(float("{0:.2f}".format(getmposapi(url,key,userid,"getusersharerate")['getusersharerate']['data'])))
    if html == 1:
        sys.stdout.write("<table><tr><td>Total Hashrate:</td><td>" + userhashrate  + "</td><td>Total Sharerate:</td><td>" + usersharerate  + "</td></tr></table>" )
    else:
        drawline(message)
        sys.stdout.write("Total hashrate: " + userhashrate  + " Total Sharerate: " + usersharerate + "\n")
if html == 1:
    sys.stdout.write("</table></body></html>")          