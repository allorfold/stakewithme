from flask import Flask, render_template, session, redirect, request, flash, jsonify, url_for
import os
from database import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as escaper
from commission import getAllTimeCommission, getDailyCommission, getCommissions, getCompleteStats, getClanStats
from better import getBetters
import hashlib, uuid
import datetime
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

# we can route to the page we want
# This is routing or mapping, tying a url to a return function
# Essentially we can load up HTML pages from this!
@app.route('/')
def home():
    return redirect('dashboard')

@app.route('/dashboard')
def dashboard():
    random = checkLogin()
    if random == 1:
        # bet, prof, paid, games, wins, loses, perc
        clandetails = getClanStats()
        return render_template('dashboard.html', notify=getNotify(), username=session['user'], pic=session['rank'],
                               clandetails=clandetails)
    elif random == 2:
        return render_template('login.html', result='You may only be logged in from one location at a time!')
    else:
        return render_template('login.html')

@app.route('/idiot')
def idiot():
    return render_template('login.html', result='You may only be logged in from one location at a time!')

@app.route('/calculator')
def calculator():
    random = checkLogin()
    if random == 1:
        return render_template('calculator.html', notify=getNotify(), username=session['user'], pic=session['rank'])
    elif random == 2:
        return render_template('login.html', result='You may only be logged in from one location at a time!')
    else:
        return render_template('login.html')

@app.route('/charts')
def charts():
    random = checkLogin()
    if random == 1:
        alltimebardata = getAllTimeCommission(session['hostid'], session['rank'])
        values = [session['user'], "Bronze", "Silver", "Gold", "All Hosts"]
        dailybardata = getDailyCommission(session['hostid'], session['rank'])
        return render_template('charts.html', notify=getNotify(), username=session['user'], pic=session['rank'],
                               alltimebardata=alltimebardata[0], dailybardata=dailybardata, averageindbardata=alltimebardata[1],
                               averagetotalbardata=alltimebardata[2],
                               values=values)
    elif random == 2:
        return render_template('login.html', result='You may only be logged in from one location at a time!')
    else:
        return render_template('login.html')

@app.route('/bettors')
def bettors():
    random = checkLogin()
    if random == 1:
        rowvalues = ["Better Name", "Total Games", "Total Wins", "Total Loses", "Win Percent", "Total Bets", "Profit", "Average Bet"]
        betterinforrows = getBetters(session['hostid'])
        return render_template('bettors.html', notify=getNotify(), rowvalues=rowvalues, username=session['user'], pic=session['rank'],
                               betterinforrows=betterinforrows[0], betterdayinforrows=betterinforrows[1])
    elif random == 2:
        return render_template('login.html', result='You may only be logged in from one location at a time!')
    else:
        return render_template('login.html')

@app.route('/host')
def host():
    random = checkLogin()
    if random == 1:
        weeks = "06/26/2016"
        allcommissions = getCommissions(session['hostid'], weeks)
        dailyvalues = ["Date", "Commission"]
        dailycommissionvalues = allcommissions[0]
        weeklyvalues = ["Week", "Commission"]
        weeklycommissionvalues = allcommissions[1]
        totalvalues = ["Name", "Total Commission", "Total Bets", "Average Bet", "Total Profit", "Total Wins", "Total Loses", "Win Percent", "North Win Percent", "South Win Percent", "Arena Percent"]
        totalcommission = getCompleteStats(session['hostid'], session['user'])
        return render_template('host.html', notify=getNotify(), username=session['user'], pic=session['rank'], dailyvalues=dailyvalues,
                               dailycommissionvalues=dailycommissionvalues, weeklyvalues=weeklyvalues,
                               weeklycommissionvalues=weeklycommissionvalues, totalcommission=totalcommission,
                               totalvalues=totalvalues)
    elif random == 2:
        return render_template('login.html', result='You may only be logged in from one location at a time!')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('dashboard')


# check to login
@app.route('/attempt', methods=['GET', 'POST'])
def attempt():

    if request.method == "GET":
        return redirect('dashboard')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            c, conn = connection()

            x = c.execute("SELECT * FROM hoster WHERE loginName = (%s)", (escaper(username)))
            if int(x) == 0:
                return render_template('login.html', result='User not found! Please contact an admin!')
            else:
                datalogin = c.fetchone()
                hashed_pass = hashlib.sha512(str(password + datalogin[4])).hexdigest()
                if(str(hashed_pass) != datalogin[3]):
                    return render_template('login.html', result='Invalid username/password. Please try again!')
                else:
                    session.clear()
                    session['user'] = datalogin[1]
                    session['hostid'] = datalogin[0]
                    session['rank'] = datalogin[5]
                    if(datalogin[5] == 'admin'):
                        session['admin'] = 1
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    c.execute("INSERT INTO logintracking (hostid, ip, timestamp) VALUES (%s, %s, %s)",
                        (int(datalogin[0]), str(request.remote_addr), str(st)))

                    randomstring = uuid.uuid4().hex
                    c.execute("UPDATE tempid SET tempid=%s WHERE hostid=%s",
                              (str(randomstring), int(datalogin[0])))
                    session['auth'] = randomstring
                    conn.commit()
                    c.close()
                    conn.close()
                    return redirect('calculator')
        except Exception as e:
            return redirect('500')


@app.route('/admin')
def admin():
    if checkLogin() == 1:
        if 'admin' in session:
            if session['admin'] == 1:
                return render_template('admin.html', username=session['user'], pic=session['rank'])
    return render_template('404.html')

@app.route('/uploadhost/<win>/<arena>', methods=['POST'])
def uploadhost(win, arena):
    checker = checkLogin()
    if(checker == 2):
        session.clear()
        return "gg"
    hostid = session['hostid']
    totalBet = float(request.form["totalbet"])
    totalPot = float(request.form["totalpot"])
    if totalBet <= 0.0:
        return "No bet"

    if win == "1":
        lose = 0
    else:
        lose = 1

    ourTimeStamp = datetime.datetime.strftime(datetime.datetime.now(),'%m/%d/%Y')
    final = ""
    c, conn = connection()

    c.execute("INSERT INTO totalbet (hostId) VALUES (%s)", (int(hostid)))
    totalbetid = c.lastrowid
    for i in range(1, 14):
        bettername = str(request.form["bettor" + str(i)]).lower()
        if(bettername != ""):
            betamount = request.form["bet" + str(i)]
            potamount = request.form["pot" + str(i)]
            if(betamount == ""):
                continue
            #return bettername + " bet " + betamount + " with the pot " + potamount
            x = c.execute("SELECT betterid FROM better WHERE betterName=%s", (str(bettername)))
            if(int(x) > 0):
                betterid = (c.fetchone())[0]
                if win == "1":
                    c.execute("UPDATE better SET totalGames = totalGames + 1, totalWins = totalWins + 1, totalBet = totalBet + %s WHERE betterid=%s", (float(betamount), int(betterid)))
                else:
                    c.execute("UPDATE better SET totalGames = totalGames + 1, totalLoses = totalLoses + 1, totalBet = totalBet + %s WHERE betterid=%s", (float(betamount), int(betterid)))
            else:
                c.execute("INSERT INTO better (betterName, totalBet, totalGames, totalWins, totalLoses) VALUES (%s, %s, 1, %s, %s)", (str(bettername), float(betamount), int(win), int(lose)))
                y = c.execute("SELECT betterid FROM better WHERE betterName=%s", (str(bettername)))
                betterid = (c.fetchone())[0]
            if win == "1":
                lose = 0
                ourprofit = float(potamount) - float(betamount)
            else:
                lose = 1
                ourprofit = 0 - float(betamount)
            c.execute("INSERT INTO bet (betAmount, betResult, betProfit, arena, timestamp) VALUES (%s, %s, %s, %s, %s)", (float(betamount), int(win), float(ourprofit), str(arena), str(ourTimeStamp)))
            betid = c.lastrowid
            c.execute("INSERT INTO bettotalbet (totalbetid, betid) VALUES (%s, %s)", (int(totalbetid), int(betid)))
            c.execute("INSERT INTO betterbet (betterid, hostid, betid) VALUES (%s, %s, %s)", (int(betterid), int(hostid), int(betid)))
            final = final + " NEXT ID " + str(betterid) + " LAST BET ID WAS " + str(betid)
    conn.commit()
    conn.close()
    return final + " TIMESTAMP " + str(ourTimeStamp) + " TOTAL " + str(totalBet) + " POT " + str(totalPot)



#New user route
@app.route('/newuser', methods=['POST'])
def newuser():
    if checkAdmin() == 0:
        return render_template('404.html')
    if request.method != "POST":
        return redirect('dashboard')
    # if checkAdmin() == 0:
    #     return redirect('dashboard')
    # adminname = session['user']
    try:
        c, conn = connection()
        hostname = escaper(request.form['hostname'])
        username = escaper(request.form['hostlogin'])
        hostrank = escaper(request.form['hostrank'])
        salt = uuid.uuid4().hex
        password = hashlib.sha512(str(request.form['password'] + salt)).hexdigest()

        x = c.execute("SELECT * FROM hoster WHERE hostName = (%s) OR loginName = (%s)", (escaper(hostname), escaper(username)))
        if int(x) > 0:
            flash("That username is already taken, please choose another!")
            return redirect('admin')
        else:
            c.execute("INSERT INTO hoster (hostName, loginName, hostPassword, hostSalt, hostRank) VALUES (%s, %s, %s, %s, %s)", (escaper(hostname), escaper(username), escaper(password), escaper(salt), escaper(hostrank)))
            conn.commit()
            newhostid = getHostId(escaper(hostname))
            c.execute("INSERT INTO tempid (hostid, tempid) VALUES (%s, %s)", (int(newhostid), str("temp")))
            conn.commit()
            conn.close()
            return redirect('admin')
    except Exception as e:
        return redirect('500')


@app.route('/500')
def e500():
    if checkLogin() == 0:
        return redirect('dashboard')
    return render_template('500.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")

def checkLogin():
    if 'user' not in session:
        return 0
    random = checkRandom()
    if random == 1:
        return 1
    elif random == 2:
        return 2
    return 0

def checkAdmin():
    if checkRandom() == 1:
        if 'admin' not in session:
            return 0
        if session['admin'] == 1:
            return 1
    return 0

def checkRandom():
    c, conn = connection()
    if 'auth' in session:
        c.execute("SELECT tempid FROM tempid WHERE hostid=%s", (str(session['hostid'])))
        datatemp = c.fetchone()
        if(datatemp[0] != session['auth']):
            session.clear()
            conn.close()
            return 2
        else:
            conn.close()
            return 1
    conn.close()
    return 0

def getHostId(hostname):
    c, conn = connection()
    x = c.execute("SELECT hostid FROM hoster WHERE hostName=%s", (str(hostname)))
    if(int(x) > 0):
        hostid = c.fetchone()
        conn.close()
        return hostid[0]
    conn.close()
    return 0

def getNotify():
    return 0

if __name__ == "__main__":
    app.run()










































