from MySQLdb import escape_string as escaper
import MySQLdb
import MySQLdb.cursors
from datetime import date, timedelta, datetime
import datetime

def getAllTimeCommission(hostid, rank):
    conn = MySQLdb.connect(user="root", passwd="Therumisgone123", db="stakeat54",
                           cursorclass=MySQLdb.cursors.SSCursor)


    cur = conn.cursor()

    cur.execute("SELECT a.*, b.*, c.hostRank, d.totalbetid FROM betterbet a JOIN bet b JOIN hoster c JOIN bettotalbet d ON a.betid=b.betid AND a.hostid=c.hostID AND d.betid=b.betid ORDER BY d.totalbetid")
    row = cur.fetchone()
    yourtotal = 0
    bronzetotal = 0
    silvertotal = 0
    goldtotal = 0
    alltotal = 0

    youravg = 0.0
    bronzeavg = 0.0
    silveravg = 0.0
    goldavg = 0.0
    totalavg = 0.0

    yourtotalbets = 0
    bronzetotalbets = 0
    silvertotalbets = 0
    goldtotalbets = 0
    totaltotalbets = 0

    yourtotalbet = 0.0
    bronzetotalbet = 0.0
    silvertotalbet = 0.0
    goldtotalbet = 0.0
    totaltotalbet = 0.0

    yoursupertotal = 0
    bronzesupertotal = 0
    silversupertotal = 0
    goldsupertotal = 0
    supersupertotal = 0

    completetotal = 0.0
    lasttotalid = 1
    lasthostid = 1
    while row is not None:
        betterid = row[0]
        hosterid = row[1]
        betid = row[2]
        betamount = row[4]
        betresult = row[5]
        betprofit = row[6]
        timestamp = row[8]
        rank = row[9]
        totalbetid = row[10]
        if(totalbetid != lasttotalid):
            #we have a new total bet!!
            if(lasthostid == hostid):
                yoursupertotal += 1
            if(lastrank == "bronze" or rank == "admin"):
                bronzesupertotal += 1
            elif(lastrank == "silver"):
                silversupertotal += 1
            elif(lastrank == "gold"):
                goldsupertotal += 1
            supersupertotal += 1
        commissionEarned = betamount * 0.1
        if(betresult == 1):
            alltotal += commissionEarned
            if(hosterid == hostid):
                # This means this bet was done by our host!!
                yourtotal += commissionEarned
            if(rank == "bronze"or rank == "admin"):
                bronzetotal += commissionEarned
            elif(rank == "silver"):
                silvertotal += commissionEarned
            elif(rank == "gold"):
                goldtotal += commissionEarned
        if(hosterid == hostid):
            yourtotalbets += 1
            yourtotalbet += betamount
        if(rank == "bronze" or rank == "admin"):
            bronzetotalbets += 1
            bronzetotalbet += betamount
        elif(rank == "silver"):
            silvertotalbets += 1
            silvertotalbet += betamount
        elif(rank == "gold"):
            goldtotalbets += 1
            goldtotalbet += betamount
        totaltotalbets += 1
        totaltotalbet += betamount
        completetotal += betamount
        lasttotalid = totalbetid
        lastrank = rank
        lasthostid = hosterid

        row = cur.fetchone()

    cur.close()
    conn.close()

    youravg = round(yourtotalbet/yourtotalbets, 2)
    bronzeavg = round(bronzetotalbet/bronzetotalbets, 2)
    silveravg = round(silvertotalbet/silvertotalbets, 2)
    goldavg = round(goldtotalbet/goldtotalbets, 2)
    totalavg = round(totaltotalbet/totaltotalbets, 2)

    yourtotalavg = round(yourtotalbet / yoursupertotal, 2)
    bronzetotalavg = round(bronzetotalbet / bronzesupertotal, 2)
    silvertotalavg = round(silvertotalbet / silversupertotal, 2)
    goldtotalavg = round(goldtotalbet / goldsupertotal, 2)
    totaltotalavg = round(totaltotalbet / supersupertotal, 2)

    return [[yourtotal, bronzetotal, silvertotal, goldtotal, alltotal], [youravg, bronzeavg, silveravg, goldavg, totalavg], [yourtotalavg, bronzetotalavg, silvertotalavg, goldtotalavg, totaltotalavg]]


def getDailyCommission(hostid, rank):
    conn = MySQLdb.connect(user="root", passwd="Therumisgone123", db="stakeat54",
                           cursorclass=MySQLdb.cursors.SSCursor)


    cur = conn.cursor()

    ourTimeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y')
    cur.execute("SELECT a.*, b.*, c.hostRank FROM betterbet a JOIN bet b JOIN hoster c ON a.betid=b.betid AND a.hostid=c.hostID WHERE b.betResult=1 AND b.timestamp=%s", (str(ourTimeStamp)))
    row = cur.fetchone()
    yourtotal = 0
    bronzetotal = 0
    silvertotal = 0
    goldtotal = 0
    alltotal = 0
    while row is not None:
        betterid = row[0]
        hosterid = row[1]
        betid = row[2]
        betamount = row[4]
        betresult = row[5]
        betprofit = row[6]
        timestamp = row[8]
        rank = row[9]
        commissionEarned = betamount * 0.1
        alltotal += commissionEarned
        if(hosterid == hostid):
            # This means this bet was done by our host!!
            yourtotal += commissionEarned
        if(rank == "bronze" or rank=="admin"):
            bronzetotal += commissionEarned
        elif(rank == "silver"):
            silvertotal += commissionEarned
        elif(rank == "gold"):
            goldtotal += commissionEarned
        row = cur.fetchone()

    cur.close()
    conn.close()

    return [yourtotal, bronzetotal, silvertotal, goldtotal, alltotal]


def getCommissions(hostid, week):
    conn = MySQLdb.connect(user="root", passwd="Therumisgone123", db="stakeat54",
                           cursorclass=MySQLdb.cursors.SSCursor)


    ourWeekStamp = datetime.datetime.strptime(week, '%m/%d/%Y')
    newIndex = week + "-" + datetime.datetime.strftime(ourWeekStamp + datetime.timedelta(6), '%m/%d/%Y')
    cur = conn.cursor()
    dailyCommissions = {}
    weeklyCommissions = {}
    totalCommission = 0.0
    weeklyCommissions[newIndex] = 0
    cur.execute(
        "SELECT a.*, b.* FROM betterbet a JOIN bet b JOIN hoster c ON a.betid=b.betid AND a.hostid=c.hostID WHERE b.betResult=1 AND a.hostid=%s ORDER BY timestamp", (int(hostid)))
    row = cur.fetchone()
    while row is not None:
        hosterid = row[1]
        betamount = row[4]
        timestamp = row[8]
        ourCurrentStamp = datetime.datetime.strptime(timestamp, '%m/%d/%Y')
        commissionEarned = betamount * 0.1
        if (hosterid == hostid):
            totalCommission += commissionEarned
            # This means this bet was done by our host!!
            if timestamp in dailyCommissions:
                dailyCommissions[timestamp] += commissionEarned
            else:
                dailyCommissions[timestamp] = commissionEarned
            if ((ourCurrentStamp - ourWeekStamp) > datetime.timedelta(6)):
                # New week!!
                newIndex = timestamp + "-" + datetime.datetime.strftime(ourCurrentStamp + datetime.timedelta(6), '%m/%d/%Y')
                weeklyCommissions[newIndex] = commissionEarned
                ourWeekStamp = ourWeekStamp + datetime.timedelta(7)
            else:
                weeklyCommissions[newIndex] += commissionEarned
        row = cur.fetchone()

    cur.close()
    conn.close()

    finalArray = []
    finalWeekArray = []

    for key, value in dailyCommissions.iteritems():
        finalArray.append([key, str(round(value, 2)) + "M"])

    for key, value in weeklyCommissions.iteritems():
        finalWeekArray.append([key, str(round(value,2)) + "M"])

    return [finalArray, finalWeekArray, totalCommission]

def getCompleteStats(hostid, name):
    #totalvalues = ["Name", "Total Commission", "Total Bets", "Total Profit", "Total Wins", "Total Loses", "Win Percent",
                  # "North Win Percent", "South Win Percent"]
    conn = MySQLdb.connect(user="root", passwd="Therumisgone123", db="stakeat54",
                           cursorclass=MySQLdb.cursors.SSCursor)


    cur = conn.cursor()
    finalArray = [name]
    cur.execute(
        "SELECT a.betterid, a.hostid, c.totalbetid, b.* FROM betterbet a JOIN bet b JOIN bettotalbet c ON a.betid=b.betid AND a.betid=c.betid AND a.hostid=%s ORDER BY c.totalbetid", (int(hostid)))
    row = cur.fetchone()
    totalcomm = 0.0
    totalbets = 0.0
    totalprofit = 0.0
    totalgames = 0
    totalwins = 0
    totalloses = 0
    northwins = 0
    northgames = 0
    southwins = 0
    southgames = 0
    arenagames = 0
    lastbetid = 0
    while row is not None:
        hosterid = row[1]
        totalbetid = row[2]
        betamount = row[4]
        betresult = row[5]
        betprofit = row[6]
        arena = row[7]
        timestamp = row[8]
        commissionEarned = betamount * 0.1
        flagging = False
        if totalbetid != lastbetid:
            flagging = True
            totalgames += 1
        totalprofit += betprofit
        totalbets += betamount
        if betresult == 1:
            if flagging:
                totalwins += 1
            totalcomm += commissionEarned
        else:
            if flagging:
                totalloses += 1
        if arena != "none":
            if flagging:
                arenagames += 1
            if arena == "north":
                if flagging:
                    northgames += 1
                if betresult == 1:
                    if flagging:
                        northwins += 1
            else:
                if flagging:
                    southgames += 1
                if betresult == 1:
                    if flagging:
                        southwins += 1
        lastbetid = totalbetid
        row = cur.fetchone()

    cur.close()
    conn.close()

    temp0 = float(northwins)
    temp1 = float(southwins)
    temp2 = float(totalwins)
    temp3 = float(arenagames)

    if northgames > 0:
        northperc = str(round(float(temp0/northgames) * 100, 2)) + "%"
    else:
        northperc = "0.0%"
    if southgames > 0:
        southperc = str(round(float(temp1/southgames) * 100, 2)) + "%"
    else:
        southperc = "0.0%"
    winpercent = str(round(float(temp2/totalgames) * 100, 2)) + "%"
    arenaperc = str(round(float(temp3/totalgames) * 100, 2)) + "%"
    avgbet = round(totalbets/totalgames, 2)

    finalArray.extend((str(round(totalcomm,2)) + "M", str(totalbets) + "M", str(avgbet) + "M", str(totalprofit) + "M", totalwins, totalloses, winpercent, northperc, southperc, arenaperc))
    print(finalArray)
    return [finalArray]


def getClanStats():
    conn = MySQLdb.connect(user="root", passwd="Therumisgone123", db="stakeat54",
                           cursorclass=MySQLdb.cursors.SSCursor)


    cur = conn.cursor()
    finalArray = []
    cur.execute(
        "SELECT sum(betamount), sum(betprofit) FROM bet")
    row = cur.fetchone()

    totalbet = row[0]
    totalprof = row[1]

    finalArray.extend((round(totalbet / 1000,2), round(totalprof / 1000,2)))
    cur.close()

    cur = conn.cursor()
    cur.execute("SELECT a.totalbetid, b.betid, b.betresult, b.betamount, b.betprofit FROM bettotalbet a JOIN bet b ON a.betid=b.betid")

    row = cur.fetchone()
    lasttotalid = 0
    totalgames = 0
    totalwins = 0
    totalloses = 0
    totalpaid = 0.0
    while row is not None:
        totalid = row[0]
        betid = row[1]
        betresult = row[2]
        betamount = row[3]
        betprofit = row[4]
        if betprofit > 0:
            totalpaid += betamount + betamount
        if(totalid != lasttotalid):
            totalgames += 1
            if betresult == 1:
                totalwins += 1
            else:
                totalloses += 1
        lasttotalid = totalid
        row = cur.fetchone()

    cur.close()
    conn.close()

    temp1 = float(totalwins)

    winperc = str(float(round(float(temp1/totalgames) * 100, 2))) + "%"
    finalArray.extend((round(totalpaid / 1000, 2), totalgames, totalwins, totalloses, winperc))

    return [finalArray]