import serial

counter = serial.Serial('/dev/counter')

counter.write(b'\x01\x36\x51\x69\x01\x0E\x01\x00\x00\x00\x6e\x34\xea\xf5')
d = counter.read(14)
dv= (d[9]<<24)+(d[8]<<16)+(d[7]<<8)+d[6]

def ieee754(f):
    return round(round(pow(-1,(f>>31))*pow(2,((f&0x7f800000)>>23)-127)*(1+(f&0x007fffff)/0x800000),3)*1000)

d = int(dv)/1000

print(d)

