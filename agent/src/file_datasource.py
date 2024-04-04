from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        with open(self.accelerometer_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.accelerometer_lines = lines
        with open(self.gps_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.gps_lines = lines
        with open(self.parking_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.parking_lines = lines

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        data = AggregatedData(
            Accelerometer(1, 2, 3),
            Gps(4, 5),
            Parking(10, Gps(1, 0)),
            datetime.now(),
            config.USER_ID,
        )
        
        if self.reading == True:
            line_len = len(self.accelerometer_lines) - 1
            if (self.acc_line > line_len):
                self.acc_line = 0
            line_len = len(self.gps_lines) - 1   
            if (self.gps_line > len(self.gps_lines) - 1):
                self.gps_line = 0
            line_len = len(self.parking_lines) - 1  
            if (self.parking_line > len(self.parking_lines) - 1):
                self.parking_line = 0

            accelerometer = self.accelerometer_lines[self.acc_line].split(',')
            gps = self.gps_lines[self.gps_line].split(',')
            parking = self.parking_lines[self.parking_line].split(',')
            
            x, y, z = accelerometer
            data.accelerometer = Accelerometer(x, y, z)
            
            latitude, longitude = gps
            data.gps = Gps(longitude, latitude)
            
            longitude, latitude, empty_count = parking
            data.parking = Parking(empty_count, Gps(longitude, latitude))
            
            self.acc_line += 1
            self.gps_line += 1
            self.parking_line +=1
        
        return data

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.reading = True
        self.acc_line = 0
        self.gps_line = 0
        self.parking_line = 0

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.reading = False
