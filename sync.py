import requests, json
import sqlite3 as db

connection = db.connect('/home/pi/tmp')
cursor = connection.cursor()

cursor.execute('select uid, sum(q) from a group by uid')
a = cursor.fetchall()
s = ''

for i in a: s = s + i[0] + ':' + str(i[1]) + ';'
s = s[0:-1]
data = {'s': s, 'st': '6'}
r = requests.post('http://agawater.ru/import', data)
response = int(r.content.decode())

if response == 0:
    cursor.execute('delete from a where id >= 0')
    connection.commit()
    cursor.execute('delete from t where id >= 0')
    connection.commit()

    r = requests.get('http://agawater.ru/getallacc')
    a = r.content.decode()
    a = a[0:-1]
    a = a.split(';')
    count = 0
    s = 'insert into t(uid, q) values '

    for i in a:
        count = count + 1
        b = i.split(':')
        s = s + "('" + b[0] + "'," + str(b[1]) + "),"

        if count == 20:
            s = s[0:-1]
            cursor.execute(s)
            connection.commit()
            
            count = 0
            s = 'insert into t(uid, q) values '

    
    if count > 0:
        s = s[0:-1]
        cursor.execute(s)
        connection.commit()
    
    print("Синхронизация выполнена...")
else:
    print("Ошибка отправки данных")
    
