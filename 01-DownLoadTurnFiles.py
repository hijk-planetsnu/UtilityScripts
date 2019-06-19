#!/usr/bin/python
'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Download PRIVATE PLAYER Game Data from PlanetNu Server.
Script accesses player's private turn data using password or APIkey.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

OBJECTIVE: Build a local 'history' of json turn files for your current running
    games. Whenever script runs it will update your local game files with
    the most recently available turn(s). When running on a game for the first
    time, it will start at turn 001 and load up to the current turn.
    
Script checks a player's game list using player name and player API key. Game data
is downloaded using the turn files from each separate game. Will access running
games in-progress and load most recent files. If you do not know your API key 
already, a code block is present to print out your API key using your username
and password as input. 

From the CWD, the data structure is:
    00-GameData/<game-name>/<turn-num>/01-RawDataDump.txt
where:
    <game-name>        = game ID number  + "-" +  game name ==> "127894-SmithsWorld"
    <turn-num>         = three char string for turn number ==> 001, 002, 003 . . .
    01-RawDataDump.txt = json turn file
.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 
CWD - - - - - - - -| 00-GameData - -| . . .
01-DownLoad..                       | 129054-Scorpius
                                    | 141666-Kattia - - | 001
                                                        | 002
                                                        | 003 -- | 01-RawDataDump.txt
.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .

Python 2.7
Use urllib2 modules for handling the http requests and returns.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
hijk/2015

'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, re, os, time
import json, urllib, urllib2, gzip, StringIO


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#    PLAYER's Personal Identifiers are required for downloading data from
#       your IN-PROGRESS games. The var "playerKEY" is the API key assigned
#       by the Planet.nu server to your account. If you do not have your key,
#       "playerKEY" should be set to "xxx" (used as a conditional flag) and  
#       your account password needs to be entered as variable "playerPASS".
#
planetNU    = 'http://api.planets.nu/'
playerNAME  = 'xxxxx'              # < planet nu username
playerKEY   = 'yyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy'               # < unknown default value should be "xxx"
playerPASS  = 'zzzzzzz'               # < only needed if playerKEY is unknown
gameData    = '001-GameData/'     # < folder name in cwd where all game data is stored; end with "/"
quickLook   = 0                   # < flag to display game List info and halt execution: 1 == yes display and exit; 0 == no download
gameRUN     = 1                   # < 0 == finished games that are publicly accessible (status=3 type=2); else 1 == current in-progress
gameStatus  = 2                   # game status 1 = joining; game status 2 = running; 3 = complete ()
gameScope   = 1                   # 0 = public; 1 = custom or private
gameTrain   = 1                   # 0 = no; 1 = yes, search training games

# Game Category Filters. Can use multiple CSV entries . . . type=1,2,3 . . . 
# Status: 1 - Joining, 2 - Running, 3 - Finished, 4 - Hold;           Default: "1,2"
# Type:   1 - Training, 2 - Standard, 3 - Team, 4 - Melee, 5 - Blitz; Default: "2,3,4"
# Scope:  0 - Public, 1 - Custom (private games);                     Default: 0


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print "\nRunning PlanetNu Game Data Retrieval . . . . \n"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 1. If player's API key is undefined as 'xxx', request key from server
#      Only use of password is for this request to get your apikey . . . . . .  .
#      Once your key is hardcoded in script, the password variable can be nullified
print "Player: ", playerNAME
if playerKEY == 'xxx':
    req = urllib2.Request(planetNU +"login?username="+playerNAME+"&password="+playerPASS )
    response = urllib2.urlopen(req)
    the_page = response.read()
    keyhunt = re.search(r'apikey\"\:\"([\w\d\-]+)\"', the_page )
    if keyhunt is not None:
        print "APIkey retrieved . . . . ",
        print "apikey: ", keyhunt.group(1)
        playerKEY = keyhunt.group(1)
else:
    print "APIkey defined: ", playerKEY


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 2. Dowload the gamelist data for player and write to temporary file . . . . . . .
#   2A = get list of current running games . . . . . .
if gameRUN == 1 and gameScope == 0:
    params = urllib.urlencode({'username':playerNAME, 'status':gameStatus})
    headers = {"Content-type": "application/x-www-form-urlencoded" }
    req = urllib2.Request(planetNU + "games/list", params, headers)
    response = urllib2.urlopen(req)
    compressedPage = StringIO.StringIO(response.read())
    decompressedPage = gzip.GzipFile(fileobj=compressedPage)
    with open("z-gamelistdata.txt", 'w') as outfile:
        outfile.write(decompressedPage.read())
        
#   2B = get list of public completed games . . . . . . . 
elif gameRUN == 0 and gameScope == 0:
    # http://api.planets.nu/games/list
    params = urllib.urlencode({'username':playerNAME, 'status':'3' })
    headers = {"Content-type": "application/x-www-form-urlencoded" }
    req = urllib2.Request(planetNU + "games/list", params, headers)
    response = urllib2.urlopen(req)
    compressedPage = StringIO.StringIO(response.read())
    decompressedPage = gzip.GzipFile(fileobj=compressedPage)
    with open("z-gamelistdata.txt", 'w') as outfile:
        outfile.write(decompressedPage.read())

#   2C = get list of current training games . . . . . . . 
elif gameTrain == 1:
    # http://api.planets.nu/games/list
    params = urllib.urlencode({'username':playerNAME, 'status':'1', 'scope':'1', 'type':'1' })
    headers = {"Content-type": "application/x-www-form-urlencoded" }
    req = urllib2.Request(planetNU + "games/list", params, headers)
    response = urllib2.urlopen(req)
    compressedPage = StringIO.StringIO(response.read())
    decompressedPage = gzip.GzipFile(fileobj=compressedPage)
    with open("z-gamelistdata.txt", 'w') as outfile:
        outfile.write(decompressedPage.read())

else:
    print "\nCheck param settings because currently there's nothing to do here . . .\n"
    sys.exit()


if quickLook == 1:
    print "\n\n------------------------------------------------------"
    IN=open("z-gamelistdata.txt")
    jsonRaw = IN.readline()
    IN.close()
    gameJson = json.loads(jsonRaw)
    print json.dumps(gameJson, indent=4)
    print "------------------------------------------------------\n\n"
    print "Game List dump flagged by quickLook == 1"
    print "Script halting via sys.exit() in loop."
    print "Set quickLook to 0 to execute beyond this step.\n\n"
    sys.exit()
    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 3. Parse the Game List data to extract game ID's, names and current turn numbers
gameName = []
gameID   = []
gameTurn = []
IN = open("z-gamelistdata.txt",'r')
gFile = IN.readline()
IN.close()
glistJson = json.loads(gFile)
#print json.dumps(glistJson, indent=4)        # < quick look at contents . . . 
Ngames = len(glistJson)
print "There are %d active games:" % len(glistJson)
for i in range(Ngames):
    gameID.append(glistJson[i]['id'])
    gameTurn.append(glistJson[i]['turn'])
    gnameX = re.sub(r'[\s\']','',glistJson[i]['name'])
    gnameX = re.sub(r'Sector','',gnameX)
    gameName.append(str(glistJson[i]['id']) + "-" + str(gnameX))
    index = i + 1
    print "     %d. %s == Game #%s at turn %s" % (index, glistJson[i]['name'], gameID[i], gameTurn[i])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 4. Download individual turn files working from the last downloaded file up to
#   the current turn. API requests are only sent for files that do not exist locally.
#   This is not a full download every time. Just the most recent files that are not
#   yet in the game data folder: "gameData".
print "\n\nRetrieving game data by Turns . . . . "
for i in range(Ngames):                         # < i loops over games in list
    print "\n\n> %s: . . . " % gameName[i]
    get = raw_input("Download Turn Files? (y/n): ")
    if (get == 'y'):
    
        if not os.path.isdir(gameData + gameName[i]):
            os.system('mkdir %s%s' % (gameData,gameName[i]))
    
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Download the Game Info package. Includes settings and scores.
        print "    - getting updated Game Info file with score data" 
        data = urllib.urlencode({'gameid':gameID[i], 'apikey':playerKEY})
        loadHeaders = {"Content-type": "application/x-www-form-urlencoded" }
        req = urllib2.Request(planetNU + "game/loadinfo?", data, loadHeaders)
        response = urllib2.urlopen(req)
        compressedPage = StringIO.StringIO(response.read())
        decompressedPage = gzip.GzipFile(fileobj=compressedPage)
        gameINFO = json.loads(decompressedPage.read())
        OUT=open("%s/%s/01-GameInfoDump.txt" % (gameData,gameName[i]), 'w')
        OUT.write(json.dumps(gameINFO, indent=4))
        OUT.close()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
        print "    - locating existing turn files: ",     
    
        if not os.path.isdir(gameData + gameName[i] + "/" + "001-TurnFiles"):
            os.system('mkdir %s%s/%s' % (gameData,gameName[i],"001-TurnFiles"))
    
        alreadyexists = 1                           # < flags when a new turn is found on server   
        for j in range(1,gameTurn[i]+1):            # < j loops over turns within a game
            numTag = str(j)
            if j < 10:
                numTag = "00"+numTag
            elif j <100:
                numTag = "0"+numTag
            turnFile = numTag + "-TurnData.txt"
            ## Check if game folder exists on local . . . . . 
            #if not os.path.isfile("%s%s/%s" % (gameData, gameName[i], turnFile)):
            #    os.system('mkdir %s%s/%s'  % (gameData, gameName[i], numTag))
                
            # Check if turn data file exists on local . . . . . 
            if os.path.isfile("%s%s/%s/%s" % (gameData, gameName[i], "001-TurnFiles", turnFile)):
                print numTag,               # < display turn number if file already exists
            else:
                # New Turn File Found . . . . . . . 
                if alreadyexists == 1:
                    print "\n    - downloading NEW turn file(s): ", numTag, 
                    alreadyexists = 0
                else:
                    print numTag,           # < display turn number of current download . . . . 
                    sys.stdout.flush()
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                # Download jth turn file . . . . . . . . . 
                data = urllib.urlencode({'gameid':gameID[i], 'apikey':playerKEY, 'turn':str(j)})
                loadHeaders = {"Content-type": "application/x-www-form-urlencoded" }
                req = urllib2.Request(planetNU + "game/loadturn?", data, loadHeaders)
                response = urllib2.urlopen(req)
                compressedPage = StringIO.StringIO(response.read())
                decompressedPage = gzip.GzipFile(fileobj=compressedPage)
                with open("%s%s/%s/%s" % (gameData, gameName[i], "001-TurnFiles", turnFile), 'w') as OUT:
                    OUT.write(decompressedPage.read())
                time.sleep(5)               # < pause between API requests
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                
                
            sys.stdout.flush()
            
        # end foreach j turn iteration
    
# end foreach i game iteration
        
print "\n\n* * * * * * *  D O N E  * * * * * * * *\n\n"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# To better look inside the json file, here's a quick way to dump contents
#   with an indented format that makes the nested data structure easier
#   to interpret.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#IN=open("00-GameData/%s/%s/01-RawDataDump.txt" % (gameName[i], numTag), 'r')
#jsonRaw = IN.readline()
#IN.close()
#gameJson = json.loads(jsonRaw)
#OUT=open("00-GameData/%s/%s/02-FormattedDataDump.txt" % (gameName[i], numTag), 'w')
#OUT.write(json.dumps(gameJson, indent=4))
#OUT.close()
##print gameJson['rst']['planets'][0]
##print gameJson['rst']['ships'][0]['name']
## sys.exit()


