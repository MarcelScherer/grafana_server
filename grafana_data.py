'''
Created on 10.06.2020

@author: Marcel
'''

import time
from dataclient_hanlder.dataclient_handler import dataclient_handler
import logging
from influxdb import InfluxDBClient
import datetime

AIR_DATA_PATH         = '192.168.2.123/data.json'
WATER_DATA_PATH       = '192.168.2.30'
WATER_DATA_PORT       = 5000


    
def air_sensor_data_handler():
    try:
        air_data_sensor = dataclient_handler(AIR_DATA_PATH)
        air_data_sensor.read_json_data('sensordatavalues', logging)
        meassured_data = air_data_sensor.get_value_list()
        print("air_data_list: " + str(meassured_data))
        return meassured_data
    except ValueError:
        logging.warn("cannot write air_data in data base")
        print ("function error air sensor")
    
def water_sensor_data_handler(): 
    try:
        water_data_sensor = dataclient_handler(WATER_DATA_PATH)
        water_value_ad = water_data_sensor.read_socket_value(WATER_DATA_PORT, 2, 2, True, '!h', 10)
        print("water_data_list: " + str(water_value_ad))
        return water_value_ad
    except ValueError:
        print ("function error")

def data_to_influx(air_data, water_data):
    try:
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'influx_data_mind')
        client.create_database('influx_data_mind') 
        if(float(air_data[2]) > 100):
            json_body = [
            {
                "measurement": "data_mind",
                "time": datetime.datetime.now() - datetime.timedelta(hours=2),
                "fields": {
                    "temp_out": ("none"),"water": (water_data[0])
                }
            }
            ] 
        else:
            json_body = [
            {
                "measurement": "data_mind",
                "time": datetime.datetime.now() - datetime.timedelta(hours=2),
                "fields": {
                    "temp_out": (float(air_data[2])),"water": (float(water_data[0]))
                }
            }
            ] 

        
        client.write_points(json_body)
    except ValueError:
        print ("function error")
    
if __name__ == '__main__': 
   logging.basicConfig(filename='grafana.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
   func_status = 1
#   while func_status == 1:
   print("start skript ...")
   try:
      air = air_sensor_data_handler()
      print(type(air[2]))
      water = water_sensor_data_handler()
      print(water[0])
      data_to_influx(air, water)
   except KeyboardInterrupt:  
      print ("Interrupt by keyboard")  
      func_status = 0
   except Exception as e:
      print("main crashed. Error: %s", e)
      logging.error("main crashed. Error: %s", e)
      time.sleep(5)
