#!/usr/bin/python
'''
SCORE TONNAGE OF SHIPS CAPTURED, ROB'd



hijk/2015

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


OUTtable=open("%s%s06-PrivateerROB.txt" % (gameData,gameName),'w')
OUTtable.write("TURN\tNEUTrob\tNumShipCap\tMassShipRob\n")
#OUTtable.close()


neutROB = 0
NumShipCap = 0
MassShipRob = 0
MCrob = 0

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
    ## SCAN MESSAGES FOR ROB MISSIONS . . . . . . 
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for j in range(len(gameJson['rst']['messages'])):
        
        match = re.search(r'boarded and captured', gameJson['rst']['messages'][j]['body'])
        if match is not None and gameJson['rst']['messages'][j]['messagetype'] == 8:
            #print "------------------------"
            #for key in ('body', 'target', 'headline', 'messagetype', 'turn', 'ownerid', 'id' ):
            #    print "   %s: %s" % (key, gameJson['rst']['messages'][j][key])
            captureID = re.search(r'ID#(\d+)', gameJson['rst']['messages'][j]['body'])
            capIDnum = int(captureID.group(1))
            ## DUMP JSON object to formatted text file . . . . . . . 
            #OUT=open("%s000-FormattedDataDump.txt" % (gameFolder), 'w')
            #OUT.write(json.dumps(gameJson, indent=4))
            #OUT.close()
            for i in range(len(gameJson['rst']['ships'])):
                if gameJson['rst']['ships'][i]['id'] == capIDnum:
                    print "   Name: ", gameJson['rst']['ships'][i]['name'], " MASS: ", gameJson['rst']['ships'][i]['mass']
                    MassShipRob += int(gameJson['rst']['ships'][i]['mass'])
                    NumShipCap += 1
                    
        match = re.search(r'(\d+) KT of their fuel', gameJson['rst']['messages'][j]['body'])
        if match is not None:
            #print "------------------------"
            #for key in ('body', 'target', 'headline', 'messagetype', 'turn', 'ownerid', 'id' ):
            #    print "   %s: %s" % (key, gameJson['rst']['messages'][j][key])
            #fuelCapture = re.search(r'(\d+) KT of their fuel', gameJson['rst']['messages'][j]['body'])
            fuelCapNum = int(match.group(1))
            neutROB += fuelCapNum

        match = re.search(r'spies', gameJson['rst']['messages'][j]['body'])
        if match is not None:
            print "------------------------"
            for key in ('body', 'target', 'headline', 'messagetype', 'turn', 'ownerid', 'id' ):
                print "   %s: %s" % (key, gameJson['rst']['messages'][j][key])
            
    OUTtable.write("%s\t%d\t%d\t%d\n" % (numTag, neutROB, NumShipCap, MassShipRob ))

print "\n\n"
print "Number of Ships Captured: ", NumShipCap
print "Ship Tonnage: ", MassShipRob
print "Fuel ROB:", neutROB
OUTtable.close()

print "\n\n\n *  *  *  *  *      D O N E     *  *  *  *  **  \n\n"


    ## Compile table of PLANET stock piles for all resources . . . . . . . 
    #OUT1=open("%s%s%s%s-PlanetStockPileDump.txt" % (gameData, gameName, planetFolder, numTag), 'w')
    #OUT1.write("Planet\tTRIT\tMOLY\tDURA\tNEUT\tSUPP\tMC\tCLANS\n")
    #for i in range(len(gameJson['rst']['planets'])):
    #    if gameJson['rst']['planets'][i]['ownerid'] == playerID:
    #        OUT1.write("%s" % gameJson['rst']['planets'][i]['id'])
    #        for res in resourceKEYS:
    #            resourcePILE[res] += gameJson['rst']['planets'][i][res]
    #            OUT1.write("\t%d" % (gameJson['rst']['planets'][i][res]))
    #        OUT1.write("\n")
    #OUT1.close()
    #
    ## Compile table of SHIP loads for all resources . . . . . . . 
    #OUT2=open("%s%s%s%s-ShipLoadFrieghter.txt" % (gameData,gameName, shipFolder, numTag), 'w')
    #OUT2.write("Ship\tTRIT\tMOLY\tDURA\tNEUT\tSUPP\tMC\tCLANS\tMINERALS\tAMMO\tBURN\tDIST\n") 
    #for i in range(len(gameJson['rst']['ships'])):
    #    if gameJson['rst']['ships'][i]['ownerid'] == playerID:
    #        beamNum = gameJson['rst']['ships'][i]['beams']
    #        torpNum = gameJson['rst']['ships'][i]['torps']
    #        # Filter Calculation on cargo transit vessels, not warships . . . . . 
    #        if beamNum <= 4 and torpNum <= 2:
    #            OUT2.write("%d" % gameJson['rst']['ships'][i]['id'])
    #            loadMass = 0
    #            mineralShip = 0
    #            for res in resourceKEYS:
    #                resourceSHIP[res] += gameJson['rst']['ships'][i][res]
    #                OUT2.write("\t%d" % (gameJson['rst']['ships'][i][res]))
    #            for res in mineralKEYS:
    #                mineralShip += gameJson['rst']['ships'][i][res]
    #            resourceSHIP['minerals'] += mineralShip
    #            OUT2.write("\t%d" % mineralShip)
    #            resourceSHIP['ammo'] += gameJson['rst']['ships'][i]['ammo']
    #            OUT2.write("\t%d" % (gameJson['rst']['ships'][i]['ammo']))
    #            # Fuel and Distance . . . . .
    #            # Did the ship move last turn . . . . .
    #            burn = 0
    #            dist = 0
    #            if len(gameJson['rst']['ships'][i]['history']) > 0:
    #                xnow  = float(gameJson['rst']['ships'][i]['x'])
    #                ynow  = float(gameJson['rst']['ships'][i]['y'])
    #                xlast = float(gameJson['rst']['ships'][i]['history'][0]['x'])
    #                ylast = float(gameJson['rst']['ships'][i]['history'][0]['y'])
    #                if (xnow != xlast or ynow != ylast) and gameJson['rst']['ships'][i]['warp'] != 0:
    #                    shipID = gameJson['rst']['ships'][i]['id']
    #                    hullID = gameJson['rst']['ships'][i]['hullid']
    #                    beamID = gameJson['rst']['ships'][i]['beamid']
    #                    torpID = gameJson['rst']['ships'][i]['torpedoid']
    #                    hullMass = gameJson['rst']['hulls'][hullID-1]['mass']
    #                    beamMass = 0
    #                    if beamID > 0:
    #                        beamMass = beamNum * gameJson['rst']['beams'][beamID-1]['mass']
    #                    torpMass = 0
    #                    if torpID > 0:
    #                        torpMass = torpNum * gameJson['rst']['torpedos'][torpID-1]['mass']
    #                    loadMass = 0
    #                    for load in massKEYS:
    #                        loadMass += gameJson['rst']['ships'][i][load]
    #                        
    #                    # First pass calcs based on current ship mass in Turn X
    #                    ShipMass = hullMass + beamMass + torpMass + loadMass   
    #                    dist = int(((xlast-xnow)**2  + (ylast-ynow)**2)**0.5)
    #                    warpX   = "warp" +  str(gameJson['rst']['ships'][i]['warp'])   # key string for warp speed
    #                    engineX = gameJson['rst']['ships'][i]['engineid']    # engine tech level 
    #                    fuelfactor = gameJson['rst']['engines'][engineX-1][warpX]
    #                    burn = int(fuelfactor * (int(ShipMass/10))/10000)
    #                    
    #                    # Now back correct for ship mass in Turn X-1 by adding burned fuel mass
    #                    ShipMass += burn
    #                    burn = int(fuelfactor * (int(ShipMass/10))/10000)
    #
    #                              
    #            resourceSHIP['burn'] += burn
    #            resourceSHIP['dist'] += dist
    #        OUT2.write("\t%d\t%d" % (burn, dist))    
    #        OUT2.write("\n")
    #OUT2.close()
    #
    #
    #OUT3=open("%s%s04-PlanetStocks.txt" % (gameData,gameName) ,'a')
    #OUT3.write(numTag)
    #for res in resourceKEYS:
    #    OUT3.write("\t%d" % resourcePILE[res])
    #OUT3.write("\n")
    #OUT3.close()
    #
    #OUT4=open("%s%s05-ShipLoads.txt" % (gameData,gameName) ,'a')
    #OUT4.write(numTag)
    #for res in resourceKEYS:
    #    OUT4.write("\t%d" % resourceSHIP[res])
    #OUT4.write("\t%d\t%d\t%d\t%d\n" % (resourceSHIP['minerals'],resourceSHIP['ammo'],resourceSHIP['burn'],resourceSHIP['dist']))
    #OUT4.close()