import socket, re, os, signal
from flask import Flask,render_template
from threading import  Thread as thread
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException



app = Flask(__name__)



def get_vehicle_first_info ():

    global status, time, date, Latitude, Longitude, type_ts1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.57", 11123))
    print ('Connected')

    pnChannel = "vehicle-tracker"

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = "sub-c-f7df9fe1-d873-4c52-b6d1-d09161021e5d"
    pnconfig.publish_key = "pub-c-8488393d-d966-4f8a-bbe9-3ec83cbb4a2f"
    pnconfig.user_id = "111"
    pnconfig.ssl = False
    
    pubnub = PubNub(pnconfig)
    pubnub.subscribe().channels(pnChannel).execute()

    Latitude_list = []
    Longitude_list = []
    gps_message_list = []


    while True:
        type_ts1 = "Vehicle 1"
        gps_message = s.recv(1024).decode()
        gps_message_list.append (gps_message)
        gps_message = gps_message.split (',')
        
        
        Latitude = gps_message [3]
        # print (Latitude)     
        lat_deg = round (float(Latitude)/100,0)
        lat_min = (float(Latitude)%100)/60
        Latitude = lat_deg + lat_min
        
        
        Longitude = gps_message [5]
        # print (Longitude)  
        lng_deg = round (float(Longitude)/100,0)
        lng_min = (float(Longitude)%100)/60
        Longitude = lng_deg + lng_min


        Latitude_list.append (Latitude)
        Longitude_list.append (Longitude)
        if len(Latitude_list) >= 3:
            try:
                Latitude_list.pop(0)
                Longitude_list.pop (0)
            except:
                pass
        try:
            if Latitude_list[1] > Latitude_list[0] or Longitude_list[1] > Longitude_list[0]:
                status = 'Move'
            else:
                status = 'Stop'
        except:
            status = 'Stop'
            pass


        date = str(gps_message [9])
        date = list(date)
        date = str(date[0])+str(date[1]) + '.' + str(date[2])+str(date[3]) + '.' + str(date[4])+str(date[5])

        time = str(gps_message [1])
        time = list(time)
        time = str(int(str(time[0])+str(time[1])) + 3) + ':' + str(time[2])+str(time[3]) + ':' + str(time[4])+str(time[5])

        print (
            type_ts1,
            'Date:', date,
            'TIME:', time,
            'Latitude:',str (Latitude) + str(gps_message[4]),
            'Longitude:', str(Longitude) + str(gps_message[6]),
            status
        )
        try:
            pubnub.publish().channel(pnChannel).message({
            'lat': Latitude,
            'lng': Longitude,
            }).sync()
        except:
            pass
        file = open('vehicle1.txt', 'w', encoding="utf-8")        
        file.write(str(gps_message_list))
  
def get_vehicle_second_info ():
    
    global status2, time2, date2, Latitude2, Longitude2, type_ts2, speed

    pnChannel = "vehicle-tracker"

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = "sub-c-f7df9fe1-d873-4c52-b6d1-d09161021e5d"
    pnconfig.publish_key = "pub-c-8488393d-d966-4f8a-bbe9-3ec83cbb4a2f"
    pnconfig.user_id = "111"
    pnconfig.ssl = False
    
    pubnub = PubNub(pnconfig)
    pubnub.subscribe().channels(pnChannel).execute()
    
    gps_message_list = []

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.1.49", 11124))
        print ('Connected')
    except:
        pass
   
    while True:
        try:
            type_ts2 = "Vehicle 2"

            gps_message = s.recv(1024).decode()
            gps_message_list.append (gps_message)
            gps_message = gps_message.split ('$')
            speed = gps_message[2]
            # print (speed)
            gps_message = gps_message[3]
            gps_message = gps_message.split (',')
            #print (gps_message)

            Latitude = gps_message [3]
            # print (Latitude)     
            lat_deg = round (float(Latitude)/100,0)
            lat_min = (float(Latitude)%100)/60
            Latitude2 = lat_deg + lat_min
            
            
            Longitude = gps_message [5]
            # print (Longitude)  
            lng_deg = round (float(Longitude)/100,0)
            lng_min = (float(Longitude)%100)/60
            Longitude2 = lng_deg + lng_min

            date = str(gps_message [9])
            date = list(date)
            date2 = str(date[0])+str(date[1]) + '.' + str(date[2])+str(date[3]) + '.' + str(date[4])+str(date[5])

            time = str(gps_message [1])
            time = list(time)
            time2 = str(int(str(time[0])+str(time[1])) + 3) + ':' + str(time[2])+str(time[3]) + ':' + str(time[4])+str(time[5])

            speed = speed.split (',')
            speed = float(speed[7])

            if speed > 0:
                status2 = 'Move'
            else:
                status2 = 'Stop'

            print (
                type_ts2,
                'Date:', date2,
                'TIME:', time2,
                'Latitude:',str (Latitude2) + str(gps_message[4]),
                'Longitude:', str(Longitude2) + str(gps_message[6]),
                'Speed', speed
            )
            file = open('vehicle2.txt', 'w', encoding="utf-8") 
            # gps_message_list.append(date)
            # print(gps_message_list)      
            file.write(str(gps_message_list))
        except:
            pass
        try:
            pubnub.publish().channel(pnChannel).message({
            'lat2': Latitude2,
            'lng2': Longitude2,

            }).sync()
            # print("publish timetoken: %d" % envelope.result.timetoken)
        except:
            pass

def send_info ():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 6669))
    print ("Working ...")
    content = "\n If you don't know what to do - write 'Help'\n Write a command:". encode()
    s.listen(5)

    while True:
    
        s2 = s.accept()
        print ('Get connected')
        pid = os.fork()
        if pid != 0:
            continue
        sock, remote = s2
        count = 0
        

        while True:
            global status, time, date, Latitude, Longitude, type_ts1
            global status2, time2, date2, Latitude2, Longitude2, type_ts2, speed
            sock.send (content) 
            line = sock.recv(1024).decode()
            # print(line)
            line = line.rstrip()

            if not line:
                sock.close()
                break

            res = re.findall(r"get info (\w+)", line)
            print(res)
            try:
                if res[0] == "vehicle1":
                    message = str ("Номер пакета: " + str(count) + "\n" + 
                                "Дата(Время)отправки: " + str(date) + "(" + str(time) + ")" + "\n" + 
                                "Идентификатор ТС: " + str(type_ts1) + "\n" + 
                                "Данные о местоположении: " + str(Longitude) + "," + str(Latitude) + "\n" + 
                                "Скорость: - \n " +
                                "Статус ТС: " + status + "\n")
                    sock.send (message.encode())
                    count =+ 1
                else:
                    if res[0] == "vehicle2":
                        message = str ("Номер пакета: " + str(count) + "\n" + 
                                    "Дата(Время)отправки: " + str(date2) + "(" + str(time2) + ")" + "\n" + 
                                    "Идентификатор ТС: " + str(type_ts2) + "\n" + 
                                    "Данные о местоположении: " + str(Longitude2) + "," + str(Latitude2) + "\n" + 
                                    "Скорость: " + str(speed) + "\n" +
                                    "Статус ТС: " + str(status2) + "\n")
                        sock.send (message.encode())
                        count =+ 1
                    else:
                        message = str ("Простите, но такого ТС в списке нет")
                        sock.send (message.encode())
                        count =+ 1
            except:
                pass

        sock.close()
                

        #sock.shutdown(socket.SHUT_RDWR)
        #break 


th1 = thread (target = get_vehicle_first_info, args = ())
th2 = thread (target = get_vehicle_second_info, args = ())
th3 = thread (target = send_info, args = ())

th1.start()
th2.start()
th3.start()

@app.route('/')
def render_map():
    global status
    return render_template('gps_map.html')	

#app.run (host = '0.0.0.0', port = 8321, debug = True)

