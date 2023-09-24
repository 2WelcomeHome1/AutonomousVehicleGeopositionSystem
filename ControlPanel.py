import socket, re, os


class ControlPanel():
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        pass
    
    def socket_connection(self, ip: str = "0.0.0.0", port: int = 6669):
        self.s.bind((ip,port))
        print ("Working ...")
        self.s.listen(5)

    def socket_connect(self):
        s2 = self.s.accept()
        print ('Get connected')
        pid = os.fork()
        return s2
    
    def _message(self,count, date, time, type_ts, Longitude, Latitude, status):
        return str ("Номер пакета: " + str(count) + "\n" + 
                    "Дата(Время)отправки: " + str(date) + "(" + str(time) + ")" + "\n" + 
                    "Идентификатор ТС: " + str(type_ts) + "\n" + 
                    "Данные о местоположении: " + str(Longitude) + "," + str(Latitude) + "\n" + 
                    "Скорость: - \n " +
                    "Статус ТС: " + status + "\n")
    
    def _vehicle_list(self):
            import json
            with open('data.json') as json_file:
                self.vehicle_list = json.load(json_file)
    
    def _send_info(self, res):
        self.sock.send (self._message(self.count, self.vehicle_list[res[0]]['Date'], self.vehicle_list[res[0]]['Time'], 
                                          res[0], self.vehicle_list[res[0]]['Longitude'],  self.vehicle_list[res[0]]['Latitude'],  
                                          self.vehicle_list[res[0]]['status']).encode())  if res[0] in self.vehicle_list else \
        self.sock.send (str ("Простите, но такого ТС в списке нет").encode())
        self.count =+ 1
        
    def control_panel (self):
        self.socket_connection()
        while True:
            self.sock, remote = self.socket_connect()
            while True:
                self.sock.send ("\n If you don't know what to do - write 'Help'\n Write a command:". encode()) 
                line = self.sock.recv(1024).decode()
                line = line.rstrip()
                if not line:
                    self.sock.close()
                    break
                
                if re.findall(r"get info (\w+)", line):
                    res = re.findall(r"get info (\w+)", line)
                    self._send_info(self, res)

            self.sock.close()