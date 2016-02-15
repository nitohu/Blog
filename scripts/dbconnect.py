import MySQLdb

def connect():
	conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="Blog")
	c = conn.cursor()

	return conn, c

if __name__ == "__main__":
	conn, c = connect()
	print("Worked")