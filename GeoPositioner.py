import socket, json
from pubnub.pubnub import PubNub
from config import PubNub_Connection
from utils import _create_date, _create_time, save_to_file, save_to_json

class GeoPositioner():
    def __init__(self, ip, port, type_ts:str = 'vehicle_1') -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pnChannel = "vehicle-tracker"
        self.Latitude_list, self.Longitude_list, self.gps_message_list = [], [], []
        self.type_ts = type_ts
        self.ip, self.port = ip, port

        self.getVehicleInfo()
        pass

    def socket_connect(self, ip: str = "", port: int = 11123):
        self.s.connect((ip,port))
        print ('Socket Connected')

    def pubnub_connect(self):
        self.pubnub = PubNub(PubNub_Connection()._pnconfig())
        self.pubnub.subscribe().channels(self.pnChannel).execute()
        print ('PubNub Connected')

    def get_vehicle_message(self):
        gps_message = self.s.recv(1024).decode()
        self.gps_message_list.append (gps_message)
        
        return gps_message.split(',')
    
    def _calc_coordinates(self, raw_data):
        lat_deg = round (float(raw_data)/100,0)
        lat_min = (float(raw_data)%100)/60

        return lat_deg + lat_min

    def __delover(self):
        if len(self.Latitude_list) >= 3:
            self.Latitude_list.pop(0)
            self.Longitude_list.pop(0)

    def _check_car_status(self):
        self.__delover()
        try: return 'Move' if (self.Latitude_list[1] > self.Latitude_list[0]) or (self.Longitude_list[1] > self.Longitude_list[0]) else 'Stop'
        except: return 'Stop'
        
    def _print_output(self, gps_message, date, time, Latitude, Longitude, status):
        print (
            self.type_ts,
            'Date:{}'.format(date),
            'TIME: %s' % time,
            f'Latitude: {str (Latitude) + str(gps_message[4])}',
            f'Longitude: {str(Longitude) + str(gps_message[6])}',
            status
        )
    
    def _send_mapmessage(self, Latitude, Longitude):
        try:self.pubnub.publish().channel(self.pnChannel).message({'lat': Latitude,'lng': Longitude}).sync()
        except:pass 

    def getVehicleInfo (self):
        self.socket_connect(self.ip, self.port)
        self.pubnub_connect()

        while True: 
            gps_message = self.get_vehicle_message()
            Latitude = self._calc_coordinates(gps_message[3])
            Longitude = self._calc_coordinates(gps_message[5])
            
            self.Latitude_list.append (Latitude)
            self.Longitude_list.append (Longitude)
            
            status = self._check_car_status()
            date = _create_date(gps_message [9])
            time = _create_time(gps_message [1])

            self._print_output(gps_message, date, time, Latitude, Longitude, status)
            self._send_mapmessage(Latitude, Longitude)
            save_to_file(self.type_ts, self.gps_message_list)
            save_to_json(self.type_ts, date, time, Longitude, Latitude, status)
