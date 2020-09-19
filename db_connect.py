import mysql.connector
import main
import settings

HOST = settings.HOST;
USER = settings.MYSQL_USER;
PASSWORD = settings.MYSQL_PASS;
DB_NAME = settings.DB_NAME;
TABLE_NAME = settings.TABLE_NAME;


def check_database(mycursor, DB_NAME):
    exist_db = False
    mycursor.execute("SHOW DATABASES")
    for db in mycursor:
        if DB_NAME in db:
            exist_db = True
            break
    return exist_db

def create_db(mycursor):
    mycursor.execute("CREATE DATABASE {NAME}".format(NAME=DB_NAME))

def check_table(mycursor, TABLE_NAME):
    exist_table = False
    mycursor.execute("SHOW TABLES")
    for table in mycursor:
        if TABLE_NAME in table:
            exist_table = True
            break
    return exist_table

def create_table(mycursor):
    query = """CREATE TABLE {TABLE} (
        track_id VARCHAR(22) NOT NULL PRIMARY KEY, 
        title TINYTEXT NOT NULL, 
        artist TINYTEXT NOT NULL,
        album TINYTEXT NOT NULL,
        duration_ms INT UNSIGNED NOT NULL,
        count SMALLINT UNSIGNED NOT NULL)
        """.format(TABLE=TABLE_NAME)
    mycursor.execute(query)

def check_song(mycursor, params):
    exist_song = False
    query = "SELECT count FROM {TABLE} WHERE track_id = %s".format(TABLE=TABLE_NAME)
    mycursor.execute(query, (params.get("track_id").rpartition(":")[-1], ))
    myresult = mycursor.fetchone()

    if myresult is not None:
        params["count"] = myresult[0] + 1
        exist_song = True
    return exist_song

def insert_record(mydb, mycursor, params):
    query = "INSERT INTO {TABLE} (track_id, title, artist, album, duration_ms, count) VALUES (%s, %s, %s, %s, %s, %s)".format(TABLE=TABLE_NAME)
    values = (params.get("track_id").rpartition(":")[-1], params.get("title"), params.get("artist"), params.get("album"), params.get("duration_ms"), params.get("count"))
    mycursor.execute(query, values)
    mydb.commit()

def update_stats(mydb, mycursor, params):
    query = "UPDATE {TABLE} SET count=%s WHERE track_id = %s".format(TABLE=TABLE_NAME)
    values = (params.get("count"), params.get("track_id").rpartition(":")[-1])
    mycursor.execute(query, values)
    mydb.commit()

def insert():
    mydb = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWORD)
    mycursor = mydb.cursor()
    db_exists = check_database(mycursor, DB_NAME)

    if not db_exists:
        create_db(mycursor)
        mycursor.close()
        mydb.close()

    mydb = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWORD, database=DB_NAME)
    mycursor = mydb.cursor()
    table_exists = check_table(mycursor, TABLE_NAME)

    if not table_exists:
        create_table(mycursor)

    track_id = main.get_track_id()
    params = {"track_id": track_id}
    song_exists = check_song(mycursor, params)

    if not song_exists:
        title, artist, album, duration = main.get_track_info(params.get("track_id"))
        params["title"] = title
        params["artist"] = artist[0]
        params["album"] = album
        params["duration_ms"] = duration
        params["count"] = 1
        insert_record(mydb, mycursor, params)
    else:
        update_stats(mydb, mycursor, params)
