import MySQLdb
import MySQLdb.cursors
from datetime import date, timedelta, datetime
import datetime

def getBetters(hostid):
    betterDict = {}
    dayDict = {}
    finalBetterDict = []
    finalDayDict = []
    conn = MySQLdb.connect(user="root", passwd="Therumisgone123", db="stakeat54",
                           cursorclass=MySQLdb.cursors.SSCursor)


    cur = conn.cursor()

    ourTimeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y')
    cur.execute(
        "SELECT a.betterid, b.*, c.bettername FROM betterbet a JOIN bet b JOIN better c ON a.betid=b.betid AND a.betterid=c.betterid WHERE hostid=%s ORDER BY betterid", (int(hostid)))
    row = cur.fetchone()
    # SCHEMA FOR DICT
    # Name, Games, Wins, Loses, Percent, Total Bets, Profit, Avg Bet
    # Name, Games, Wins, Loses, Total Bets, Profit
    while row is not None:
        betterid = row[0]
        betid = row[1]
        betamount = row[2]
        betresult = row[3]
        betprofit = row[4]
        timestamp = row[6]
        bettername = row[7]
        if ourTimeStamp == timestamp:
            if bettername in dayDict:
                dayDict[bettername][1] += 1
                if betresult == 1:
                    dayDict[bettername][2] += 1
                else:
                    dayDict[bettername][3] += 1
                dayDict[bettername][4] += betamount
                dayDict[bettername][5] += betprofit
            else:
                if betresult == 1:
                    dayDict[bettername] = [bettername, 1, 1, 0, betamount, betprofit]
                else:
                    dayDict[bettername] = [bettername, 1, 0, 1, betamount, betprofit]

        if bettername in betterDict:
            betterDict[bettername][1] += 1
            if betresult == 1:
                betterDict[bettername][2] += 1
            else:
                betterDict[bettername][3] += 1
            betterDict[bettername][4] += betamount
            betterDict[bettername][5] += betprofit
        else:
            if betresult == 1:
                betterDict[bettername] = [bettername, 1, 1, 0, betamount, betprofit]
            else:
                betterDict[bettername] = [bettername, 1, 0, 1, betamount, betprofit]
        row = cur.fetchone()

    for value in betterDict.itervalues():
        if(value[2] > 0):
            #percent = "THERE ARE " + str(value[2]) + " BY " + str(value[1])
            temp = float(value[2])
            percent = round(temp/value[1] * 100, 2)
        else:
            percent = 0.0
        avgbet = round(float(value[4]/value[1]), 2)
        finalBetterDict.append([value[0], value[1], value[2], value[3], str(percent) + "%", str(value[4]), str(value[5]), str(avgbet)])

    for value in dayDict.itervalues():
        if (value[2] > 0):
            # percent = "THERE ARE " + str(value[2]) + " BY " + str(value[1])
            temp = float(value[2])
            percent = round(temp / value[1] * 100, 2)
        else:
            percent = 0.0
        avgbet = round(float(value[4] / value[1]), 2)
        finalDayDict.append(
            [value[0], value[1], value[2], value[3], str(percent) + "%", str(value[4]), str(value[5]), str(avgbet)])

    return [finalBetterDict, finalDayDict]