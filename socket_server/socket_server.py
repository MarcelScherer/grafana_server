'''
Created on 26.03.2018

@author: Marcel
'''
import socket
from datetime import date, datetime
from datetime import timedelta
import struct
from threading import Thread

class socket_server(Thread):
    def __init__(self, ip_address, port, stuct_type):
        Thread.__init__(self)                                                                       # create a own thread with the run-function
        self.deamon = True                                                                          # thread as deamon
        self.ip_address = ip_address                                                                # store ip from data server
        self.port       = port                                                                      # store port from data server
        self.stuct_type = stuct_type                                                                # struct type for send data
        self.data_list = []                                                                         # data list for send data
        self.start()
        
    def run(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                       # create tcp socket 
        self.serversocket.bind((self.ip_address, self.port))                                        # bind socket on fix port
        self.serversocket.listen(5)                                                                 # set maximum listeners
        while(True):            
            self.connection, client_address = self.serversocket.accept()                            # wait for connection ...
            print "connection ..."
            if (len(self.data_list) > 0):                                                           # if send data list not zero
                print("send data: " + str(self.data_list))
                for element in range(0,len(self.data_list)):                                        # convert all values in float and send ...
                    print(str(self.data_list[element]))
                    self.connection.send(struct.pack(self.stuct_type,float(str(self.data_list[element]))))
            self.connection.close()                                                                 # close connection and wait for next client
            
    def update_data_list(self, data_list):
        print "update data: " + str(len(data_list))
        self.data_list = data_list                                                                  # update send data list