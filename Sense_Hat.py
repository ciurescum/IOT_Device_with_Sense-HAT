#!/usr/bin/env python

from sense_hat import SenseHat
from datetime import datetime
from time import strftime
import time
import MySQLdb

timestamp=datetime.now()
sense=SenseHat()

db = MySQLdb.connect(host="localhost", user="root",passwd="1234", db="IoT_database")
cur = db.cursor()

def get_sense_data():
    sense_data=[]
    sense_data.append(round(sense.get_temperature(),2))
    sense_data.append(round(sense.get_pressure(),2))
    sense_data.append(round(sense.get_humidity(),2))

    orientation = sense.get_orientation()
    sense_data.append(orientation["yaw"])
    sense_data.append(orientation["pitch"])
    sense_data.append(orientation["roll"])

    mag=sense.get_compass_raw()
    sense_data.append(mag["x"])
    sense_data.append(mag["y"])
    sense_data.append(mag["z"])

    acc = sense.get_accelerometer_raw()
    sense_data.append(acc["x"])
    sense_data.append(acc["y"])
    sense_data.append(acc["z"])

    gyro = sense.get_gyroscope_raw()
    sense_data.append(gyro["x"])
    sense_data.append(gyro["y"])
    sense_data.append(gyro["z"])

    sense_data.append(datetime.now())
    return sense_data

while True:
    param = get_sense_data()
    #print param
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    #print datetimeWrite
    x=[0,255,0]
    o=[0,0,0]
    matrice_pixeli=[o, o, o, o, o, o, o, o,  o, o, o, o, o, o, o, x,  o, o, o, o, o, o, x, o,  o, o, o, o, o, x, o, o,  o, o, x, o, x, o, o, o,  o, o, o, x, o, o, o, o,  o, o, o, o, o, o, o, o,  o, o, o, o, o, o, o, o]
    msg="!"
    if float(param[1])>32.5:
        sense.show_message(msg, scroll_speed=1, text_colour=[255,0,0])
    else:
        sense.set_pixels(matrice_pixeli)
    orientare = sense.get_orientation()
    p=round(orientare["pitch"],2)
    r=round(orientare["roll"],2)
    y=round(orientare["yaw"],2)
    print orientare
    sql = ("""INSERT INTO parametri (data,temperatura,presiune,umiditate, pitch, roll, yaw) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(datetimeWrite,param[0],param[1],param[2],p,r,y))
    try:
        print "Writing to database..."
        # Execute the SQL command
        cur.execute(*sql)
        # Commit your changes in the database
        db.commit()
        print "Write Complete"

    except:
        # Rollback in case there is any error
        db.rollback()
        print "Failed writing to database"

    cur.close()
    db.close()
    break;
