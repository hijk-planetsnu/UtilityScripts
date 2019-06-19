#!/usr/bin/python
'''
SCAN MESSAGES FOR BIRD MAN SPY MISSIONS:

    # - - - - - - - - - - - - - - - - -
    <<< Planetary Message >>>
    Distress CALL!
    From: Planet of the Apes
    We have found spies on the planet.
    They have CHANGED the planet's
    friendly code!
    The code is now: LFm
    
    # - - - - - - - - - - - - - - - - -
    <<< Planetary Message >>>
    From: Kthislmup
    We have found spies on the planet.
    They have the planet's friendly code!
    
    # - - - - - - - - - - - - - - - - -
    <<< Planetary Message >>>
    Distress CALL!
    From: Planet of the Apes
    We have found spies on the planet.
    They have CHANGED the planet's friendly code!
    The code is now: LFm
    Defense outposts using an
    ion discharge overload to
    decloak all ships in orbit.
    Ten outposts sacrificed.



hijk/2016

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
gameData = '001-GameData/'
gameName = '151485-MemoryAlpha/'
testDump = 0    # flag to output formatted data file
turnFolder = "001-TurnFiles/"

gameFolder = gameData + gameName + turnFolder        #  '00-GameData/127256-SmithsWorld'
turnFiles  = [f for f in os.listdir(gameFolder) if re.match(r'\d\d\d-TurnData', f)]

OUTtable=open("%s%s07-BirdManSpy.txt" % (gameData,gameName),'w')

for turn in turnFiles:
    print turn
    numTagchars = re.match(r'^(\d\d\d)',turn)
    if numTagchars is None: break
    numTag = numTagchars.group(1)
    
    IN=open("%s%s" % (gameFolder, turn), 'r')
    jsonRaw = IN.readline()
    IN.close()
    gameJson = json.loads(jsonRaw)
    playerID = gameJson['rst']['player']['id']
    
    if testDump == 1 and len(gameJson['rst']['ships']) > 20:
        OUT=open("%s/FormattedDataDump-%s.txt" % (gameFolder, turn), 'w')
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
        sys.exit()
        
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## SCAN MESSAGES FOR BIRD SPY MISSIONS . . . . . . 
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for j in range(len(gameJson['rst']['messages'])):
        match1 = re.search(r'friendly code', gameJson['rst']['messages'][j]['body'])
        match2 = re.search(r'ion discharge', gameJson['rst']['messages'][j]['body'])
        if match1 is not None or match2 is not None:
            print "------------------------"
            OUTtable.write("- - - - - - - - - - - - - - - - -\n")
            for key in ('body', 'target', 'headline', 'messagetype', 'turn', 'ownerid', 'id' ):
                print "   %s: %s" % (key, gameJson['rst']['messages'][j][key])
                OUTtable.write("   %s: %s\n" % (key, gameJson['rst']['messages'][j][key]))

OUTtable.close()

print "\n\n\n *  *  *  *  *      D O N E     *  *  *  *  **  \n\n"


 