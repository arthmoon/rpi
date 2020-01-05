import serial, time


ibtn = serial.Serial('/dev/arduino', 9600, timeout=1)

uid = ''

while True:
    uid = 'none'
    try:
        ibtn.write("0".encode())
        if(ibtn.inWaiting() > 0):
            uid = ibtn.readline().decode()[:-2]
            print(uid)
    except:
        print('serial port exception. data could not be read')

    time.sleep(1)
