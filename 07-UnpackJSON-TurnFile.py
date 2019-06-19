#!/usr/bin/python
'''
Just unpack a single JSON turn file into a formatted text file.

Try the online JSON viewer:
    http://jsonviewer.stack.hu/

hijk/2018

'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, re, os, time
import json, urllib, urllib2, gzip, StringIO

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# To better look inside the json file, here's a quick way to dump contents
#   with an indented format that makes the nested data structure easier
#   to interpret.
#       gameJson = json.loads(jsonRaw)
#       json.dumps(gameJson, indent=4)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
gameData   = '001-GameData/'
gameName   = '310942-BIRD-043/'
turnDump   = '005'
turnFolder = "001-TurnFiles"

gameFolder = gameData + gameName + turnFolder        #  '00-GameData/127256-SmithsWorld'
print "\n\nCracking Open: %s for Turn %s . . ." % (gameName, turnDump)

IN=open("%s/%s-TurnData.txt" % (gameFolder, turnDump), 'r')
jsonRaw = IN.readline()
IN.close()
gameJson = json.loads(jsonRaw)
playerID = gameJson['rst']['player']['id']


OUT=open("%s/FormattedDataDump-%s.txt" % (gameFolder, turnDump), 'w')
OUT.write(json.dumps(gameJson, indent=4))
OUT.close()
print "username              = ", gameJson['rst']['player']['username']
print "race id num           = ", gameJson['rst']['player']['raceid']
print "player number in game = ", gameJson['rst']['player']['id']
#print gameJson['rst']['ships'][0]['name']
print len(gameJson['rst']['ships'])
for i in range(len(gameJson['rst']['ships'])):
    print gameJson['rst']['ships'][i]['name'], gameJson['rst']['ships'][i]['ownerid']

# DUMP JSON object to formatted text file . . . . . . . 
OUT=open("%s000-FormattedDataDump.txt" % (gameFolder), 'w')
OUT.write(json.dumps(gameJson, indent=4))
OUT.close()

print "\nCompleted . . . .\n"

