from flask import Flask,render_template
from threading import  Thread as thread
from GeoPositioner import GeoPositioner

from ControlPanel import ControlPanel

class AutonomousVehicle():
    def __init__(self,ip, port) -> None:
        # self.id=id
        self.ip, self.port = ip, port
        
        self.create_thread()
        pass

    def add_new_vehicle(self): #Создать ТС
        pass

    def delete_vehicle(self): #Удалить ТС
        pass

    def create_thread(self): #Создать поток для отслеживания ТС
        th1 = thread (target = GeoPositioner, args = (self.ip, self.port, 'vehicle_1'))
        th2 = thread (target = ControlPanel().control_panel, args = ())

        th1.start()
        th2.start()
        pass
    
    def run_by_vehicle(self): #Запустить позиционирование ТС
        pass
    
    def get_vehicle_info(self): #Получить информацию о ТС
        pass

    def save_data(self): # Сохранять json
        pass


if __name__ == '__main__':
    app = Flask(__name__)
    AutonomousVehicle('1.1.1.1', 1922).create_thread()
    @app.route('/')
    def render_map():
        return render_template('gps_map.html')	
    app.run (host = '0.0.0.0', port = 8321)