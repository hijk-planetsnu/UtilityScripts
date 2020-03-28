#!/usr/bin/python
'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
CREATE A CUSTOM GAME
Quick setup for practice 1 Human vs 10 Computer Players

hijk/2018/2019
'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, re, os, time
import json, urllib, urllib2, gzip, StringIO
import datetime

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Runtime Variables . . . . . . . . . . 
# Define the Human Player race . . . .
gameName="COM-043"
gameDescrip="Training Exercise - Small Circle"

# Define Player RACES . . . .
# 1 = Federation; 2 = Lizards; 3 = Birds; 4 = Fascists; 5 = Privateers; 6 = Cyborg; 7 = Crystals; 8 = Empire; 9 = Robots; 10 = Rebels; 11 = Colonies; 12 = Horwasp.
hrace    = 11                # human player race
craces   = [ 1, 10, 3]       # computer players
numCRs   = len(craces)
mapunits = 200 + 200*(numCRs+1)
planetN  = 10  + 30*(numCRs+1)
PLSqueue = "y"   #  "y/n", else PBP points
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Fixed Variables . . . . . . . . . . . . . 
planetNU    = 'http://api.planets.nu/'
createGame  = 'account/createcustomgame?'
playerNAME  = '_____________'    # < planet nu username
playerKEY   = 'xxx'              # < need to use the 01 utility script to find your api-key.
paramFile   = "CreateCustomGameDefaults-v4-PPQ.txt"

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
# 1. Define the player list id's and raceid's . . . . . . . .
# https://stackoverflow.com/questions/46709654/urlencode-list-of-dictionaries
# https://stackoverflow.com/questions/36640573/how-to-urllib-urlencode-a-dictionary-within-an-array
# urlencoding characters:
#   %3A = :    %27 = '   %2C = ,  + = space
#

print("Player Data Array:")
P = []
P.append({})
P[0]['id'] = '1'
P[0]['raceid'] = '%d' % hrace
for i in range(len(craces)):
    P.append({})
    P[i+1]['id'] = '%d' % (i+2)
    P[i+1]['raceid'] = '%d' % (100+craces[i])

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 2. Load the game parameter string . . . . . . . .
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
S['numplayers']  = numCRs + 1
S['mapheight']   = mapunits
S['mapwidth']    = mapunits
S['numplanets']  = planetN

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
gameSettings = re.sub(r'%27','%22',gameSettings)   # deletes all single-quotes

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 3. Form the http request string . . . . . .
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
    response = decompressedPage.read()
    responseitems = response.split(",")
    outprint = re.sub('{', '', responseitems[0])
    print("\n>>>------------------\nGame Creation Request Status: \n                              %s\n>>>---------------------\n\n" % outprint)
    with open("z-log-CreateCustomGame.txt",'a') as LOG:
        LOG.write("%s\t%s\t%s\n" % (datetime.date.today(), gameName, hrace))
except IOError:
    print("\n>>>------------------\nError Creating Game:\n%s\n>>>---------------------\n\n" % compressedPage.read())
        
print "\n\n* * * * * * *  D O N E  * * * * * * * *\n\n"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



