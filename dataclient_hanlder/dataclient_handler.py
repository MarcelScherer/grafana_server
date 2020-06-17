'''
Created on 17.03.2018

@author: Marcel
'''
import requests
import json
from socket import *
import struct
import time

class dataclient_handler(object):
    def __init__(self, ip_address):
        self.ip_address = ip_address                                                                # store ip from data server
        self.parameter_list = []                                                                    # global emty parameter list
        self.value_list = []                                                                        # global emty value list for received values
        
    def read_json_data(self, key, logger):
        try:
            request = requests.get('http://' + self.ip_address)                                     # configure json request
            json_obj =  json.loads(request.content)                                                 # laod jason data
            json_data = json_obj.get(key)                                                           # read data list from dictonary with key 
            self.parameter_list = []
            self.value_list = []
            for index in range(0,len(json_data)):                                                   # sort all data in a ...
                self.parameter_list.append(json_data[index].get('value_type'))                      # ... parameter list ...
                self.value_list.append(json_data[index].get('value'))                               # ... and value list
        except:
            logger.warn('cannot read json data')
    
    def read_socket_value(self, port, num_of_byte, byte_per_value,init_send, convert_type, timeout_time):
        clientsocket = socket(AF_INET, SOCK_STREAM)                                                 # create socket
        clientsocket.connect((self.ip_address, port))                                               # connect socket as client 
        if(init_send == True):                                                                      # is init_send flag is true
            clientsocket.send(b'1')                                                                    # send a default "1"
        data_buffer = ""
        data_value = []
        deadline = time.time() + timeout_time
        while(len(data_buffer) < num_of_byte and (time.time() < deadline)):                        # read in buffer till all data received
            data_buffer += clientsocket.recv(num_of_byte-len(data_buffer))
        for i in range(0,num_of_byte/byte_per_value):
            data_value.append(struct.unpack(convert_type, data_buffer[i*byte_per_value:i*byte_per_value+byte_per_value])[0]) # convert binary in fix type 
        return data_value                                                                          # return value
        

    def get_parameter_list(self):
        return self.parameter_list
    
    def get_value_list(self):
        return self.value_list




        
        
    
