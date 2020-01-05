import RPi.GPIO as GPIO
import serial, time
import sqlite3 as db

pin = 11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

ibtn = serial.Serial('/dev/arduino', 9600, timeout = 1)
counter = serial.Serial('/dev/counter', 9600, timeout = 3)
counter_addr = b'\x01\x36\x51\x69\x01\x0E\x01\x00\x00\x00\x6e\x34\xea\xf5'

GPIO.output(pin, True)

connection = db.connect('/home/pi/tmp')
cursor = connection.cursor()

opened = False
current_uid = ''
dq = 0
q1 = 0
q2 = 0

def printlog(message):
    #f = open("/home/pi/water.log","a")
    #f.write(time.strftime("%H:%M:%S") + "> " + message + "\n")
    #f.close()
    print(time.strftime("%H:%M:%S") + "> " + message)

def ieee754(f):
    return round(round(pow(-1,(f>>31))*pow(2,((f&0x7f800000)>>23)-127)*(1+(f&0x007fffff)/0x800000),3)*1000)

printlog('Начало работы. Клапан закрыт...')

none_try = 0;

while True:
    uid = 'none'
    try:
        ibtn.write("0".encode())
        if (ibtn.in_waiting > 0):
            uid = ibtn.readline().decode()[:-2]

    except:
        printlog('Ошибка чтения ардуино...')

    if (current_uid != '' and uid != 'none'):
        uid = current_uid

    #printlog(uid)

    if (uid != 'none'):
        if not opened:
            cursor.execute('select t.uid, (t.q - ifnull(b.q,0)) as q from t left join (select uid, sum(q) as q from a group by uid) b on b .uid = t.uid where t.uid = :uid', {'uid': uid})
            row = cursor.fetchone()
            if (row is None): q = 0
            else: q = row[1]

            if q > 0:
                dq = 0

                counter.write(counter_addr)
                d = counter.read(14)
                dv= int((d[9]<<24)+(d[8]<<16)+(d[7]<<8)+d[6]) 
                q1= dv
                q2= q1

                GPIO.output(pin, False)
                opened = True
                current_uid = uid

                #print("Клапан открыт для ", current_uid)
                #print("Доступный лимит: ", q)
                printlog("Клапан открыт для: " + current_uid)
                printlog("Доступный лимит: " + str(q))
        else:
            counter.write(counter_addr)
            d = counter.read(14)
            dv= int((d[9]<<24)+(d[8]<<16)+(d[7]<<8)+d[6]) 
            q2= dv
            dq= q2 - q1

            #print("Воды получено: ", dq)

            if dq >= 60 or dq >= q or uid != current_uid or dq < 0:
                try:
                    cursor.execute("insert into a(uid,q) values(:uid,:q)", {"uid": current_uid, 'q': dq})
                    connection.commit()
                except:
                    printlog("Ошибка сохранения данных")

                GPIO.output(pin, True)
                opened = False
                current_uid = ""
                printlog("Воды получено: " + str(dq))
                printlog("Клапан закрыт. Ждем...")
    else:
        if (opened):
            if (none_try < 2):
                none_try = none_try + 1
                time.sleep(0.5)
                continue

            try:
                cursor.execute("insert into a(uid,q) values(:uid,:q)", {"uid": current_uid, 'q': dq})
                connection.commit()
            except:
                print('Ошибка сохранения данных')

            none_try = 0
            GPIO.output(pin, True)
            opened = False
            current_uid = ""
            #print("Воды получено: ", dq)
            #print("Клапан закрыт. Ждем...")
            printlog("Воды получено: " + str(dq))
            printlog("Клапан закрыт. Ждем...")

    time.sleep(0.5)


