#!/usr/bin/python
'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
CREATE A CUSTOM GAME - KILL CIRCLE Training Exercise . . . . . . . . . . . . . 
Quick setup for practice 1 Human vs a team of Computer Players.
   Game settings use a default list from an input file: "CreateCustomGamesDefaults.txt"
   The most likely variables you want to change between games are input in VAR section.
        Inputs:  - define the race you want to play
                 - set the number of computer AIs
                 - define the computer races
Defaults in this script are set for kill circle with human in center. Map size and number of planets are
    calculated based on the number of player races: 40 planets per player, 250 map units per player.

hijk/2018
'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, re, os, time
import json, urllib, urllib2, gzip, StringIO
import datetime

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Runtime Variables . . . . . . . . . .
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
gameName    = "BIRD-013"
gameDescrip = "Kill Circle Training Exercise"

# optional: pass gameName as command line argument . . . . . 
if (len(sys.argv) > 1):
    gameName = sys.argv[1]

# Define Player RACES . . . .
# 1 = Federation; 2 = Lizards; 3 = Birds; 4 = Fascists; 5 = Privateers; 6 = Cyborg; 7 = Crystals; 8 = Empire; 9 = Robots; 10 = Rebels; 11 = Colonies; 12 = Horwasp.
hrace    = 3                  # Team 1 = human player race in center of map
craces   = [ 1, 2, 11, 9 ]    # Team 2 = encircling computer races
numCRs   = len(craces)
mapunits = 600 + 240*(numCRs+1)
planetN  = 50  +  45*(numCRs+1)
PLSqueue = "y"   #  "y/n", else PBP points

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Fixed Variables . . . . . . . . . . . . . 
planetNU    = 'http://api.planets.nu/'
createGame  = 'account/createcustomgame?'
playerNAME  = 'xxxxx'                                    # < planet nu username
playerKEY   = 'yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy'    # < unknown default value should be "xxx"  
paramFile   = "CreateCustomGameDefaults-KillCircle-PLS.txt"
if (PLSqueue == 'n'):
    paramFile = "CreateCustomGameDefaults-KillCircle.txt"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print "\nCreating Custom Private Game . . . . \n"

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 1. Set apikey . . . . . . . . 
D = {}
D['name']    = playerNAME
D['apikey']  = playerKEY
gameUser = urllib.urlencode(D)
print("\nAPIKEY setup . . . ")
print("   >%s<" %gameUser)

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 2. Define the player list id's and raceid's . . . . . . . .
print("Player Data Array:")
P = []
P.append({})
P[0]['id'] = '1'
P[0]['raceid'] = '%d' % hrace
P[0]['teamid'] = '1'
for i in range(len(craces)):
    P.append({})
    P[i+1]['id'] = '%d' % (i+2)
    P[i+1]['raceid'] = '%d' % (100+craces[i])
    P[i+1]['teamid'] = '2'


# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 3. Load the game parameter string . . . . . . . .
S = {}
# Add the key vars that are unique to this practice game . . . . . . 
S['name']        = gameName
S['description'] = gameDescrip
S['players']     = P
# Read file of standard game settings that are not likely to change from one game to next,
#   or edit the game settings directly within that file.
IN1 = open(paramFile)
count = 3
for line in IN1:
    if not (re.match(r'#',line) or len(line) < 3):
        d = line.rstrip().split(':')
        S[d[0]] = d[1].strip()
        count += 1

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 4. Compile json request string with the data for each game setting . . . . . . .
#    Make any runtime changes to setting vars. 
#    - overwrite var settings in parameter file for these keys.
#    - see Planet Density Calc to adjust if needed: http://planets.nu/_library/whisperer-scripts/planetdensity.html
S['numplayers'] = numCRs + 1
S['mapheight']  = mapunits
S['mapwidth']   = mapunits
S['numplanets'] = planetN

# List to screen all settings values . . . . . . . .
print("\nGame Settings:")
count = 1
for k,v in S.iteritems():
    print "   %d   |%s:%s|" % (count,k,v)
    count += 1

print("\n-- - - -- --- - - - -- -- - --- --- - - - - - -- --")
print("There were %s game settings loaded." % (count-1))
print("-- - - -- --- - - - -- -- - --- --- - - - - - -- --")
gameSettings = urllib.urlencode({'settings': S})
gameSettings = re.sub(r'%27','%22',gameSettings)   # replace single-quotes with double-quotes

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 5. SEND HTTP request string . . . . . .
print("\n\nSENDING: request to create game \"%s\" . . . . " % gameName)
#print("\n\n%s%s%s&%s\n\n" % (planetNU,createGame,gameUser,gameSettings))
req = urllib2.Request(planetNU + createGame, "%s&%s" % (gameUser,gameSettings) )
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urllib2.urlopen(req)
compressedPage = StringIO.StringIO(response.read())
try:
    decompressedPage = gzip.GzipFile(fileobj=compressedPage)
    #with open("createLog.txt", 'w') as OUT:
    #    OUT.write(decompressedPage.read())
    print("\n>>>------------------\nGame Created:\n%s\n>>>---------------------\n\n" % decompressedPage.read())
    with open("z-log-CreateCustomGame.txt",'a') as LOG:
        LOG.write("%s\t%s\t%s\n" % (datetime.date.today(), gameName, hrace))
except IOError:
    print("\n>>>------------------\nError Creating Game:\n%s\n>>>---------------------\n\n" % compressedPage.read())
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

print "\n\n* * * * * * *  D O N E  * * * * * * * *\n\n"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


