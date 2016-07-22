import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="Therumisgone123", db="stakeat54")
    c = conn.cursor()
    return c, conn