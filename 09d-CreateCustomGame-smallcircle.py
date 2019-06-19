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
gameName="BIRD-044"
gameDescrip="Training Exercise"

# Define Player RACES . . . .
# 1 = Federation; 2 = Lizards; 3 = Birds; 4 = Fascists; 5 = Privateers; 6 = Cyborg; 7 = Crystals; 8 = Empire; 9 = Robots; 10 = Rebels; 11 = Colonies; 12 = Horwasp.
hrace    = 3                 # human player race
craces   = [ 1, 2, 11]       # computer players
numCRs   = len(craces)
mapunits = 200 + 250*(numCRs+1)
planetN  = 20  +  40*(numCRs+1)
PLSqueue = "y"   #  "y/n", else PBP points
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Fixed Variables . . . . . . . . . . . . . 
planetNU    = 'http://api.planets.nu/'
createGame  = 'account/createcustomgame?'
playerNAME  = 'xxxxxxx'                                    # < planet nu username
playerKEY   = 'yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy'    # < unknown default value should be "xxx"  
paramFile   = "CreateCustomGameDefaults-v3-PLS.txt"

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

# for p in P:        
#     playerDefs.append(urllib.urlencode({ k: json.dumps(v) for k,v in p.iteritems() }))
#     #playerDefs.append({ k: json.dumps(v) for k,v in p.iteritems() })
# print("    Player ID String as List of Dictionaries:")
# print(P)
print("     Done.")
#players=%5B%7B%27id%27%3A+1%2C+%27raceid%27%3A+101%7D%2C+%7B%27id%27%3A+2%2C+%27raceid%27%3A+102%7D%2C
#players=[   {  ' id '  :  1 ,   ' raceid '  :  101 }  ,   {  ' id '  :  2 ,   ' raceid '  :  102 }  ,
#players=[{'id': 1, 'raceid': 101}, {'id': 2, 'raceid': 102}, . . .

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
#gameSettings = re.sub(r'%3A+','%3A',gameSettings)    # deletes all spaces
#gameSettings = re.sub(r'%2C','%3B',gameSettings)   # convert , to ;
#gameSettings = re.sub(r'%22','',gameSettings)   # delete "

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
    print("\n>>>------------------\nGame Created:\n%s\n>>>---------------------\n\n" % decompressedPage.read())
    with open("z-log-CreateCustomGame.txt",'a') as LOG:
        LOG.write("%s\t%s\t%s\n" % (datetime.date.today(), gameName, hrace))
except IOError:
    print("\n>>>------------------\nError Creating Game:\n%s\n>>>---------------------\n\n" % compressedPage.read())
        
print "\n\n* * * * * * *  D O N E  * * * * * * * *\n\n"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# wincondition=1
# minrank=1
# maxrank=6
# mintenacity=80
# hostdays=_M_W__S
# hostime=20:00
# faststart=15
# campaignmode=false
# maxadvantage=500
# fascistdoublebeams=true
# superspyadvanced=true	
# starbasefightertransfer=true	
# cloakandintercept=true 	
# productionqueue=true 	
# productioncost=1
# productionvalue=2
# productionreward=2
# killrace=true	
# fightorfail=0
# fofincrement=3
# stealth=false 	
# combatrng=0
# fcodesmustmatchgsx=true 	
# fcodesextraalchemy=true
# fcodesbdx=true
# isprivate=true 	
# password=""
# numplayers=11
# maxallies=1
# maxshareintel=3
# maxsafepassage=3
# maxplayersperrace=1
# mapshape=0
# mapwidth=2150
# mapheight=2150
# sphere=false
# homeworldlocations=2
# verycloseplanets=3
# closeplanets=12
# otherplanetsdist=155
# homestarbase=true
# homeresources=3
# homeclans=25000
# extraplanets=0
# extraships=0
# shiplimit=500
# planetscanrange=10000
# shipscanrange=300
# numplanets=500
# numstars=2
# numnebulas=2
# numdebris=2
# maxionstorms=4
# nuionstorms=true 	
# maxwormholes=10
# wormholemix=80
# wormholescanrange=100
# mineraldensity=2
# nativeprobability=60
# nativegovernmentlevel=2
# nativeclansmin=1000
# nativeclansmax=75000
# centerextraplanets=1
# centerextraships=1
# teams=0
# shuffleteampositions=false
# disallowedraces="12"
# crystalwebimmunity=0
# emorkslegacy=false


