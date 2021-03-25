import sys, os
from src.utils.utils import Utils

import logging
import socket
import threading    
import json
import time

BASE_PIPELINE_PATH = os.path.dirname(os.path.realpath(__file__)).split("src")[0]

########################################
# Base class for all dccs socket server
########################################
class BaseSocketServer(object):

    CONFIG_PATH = BASE_PIPELINE_PATH +"src/config/config.json"

    CONNECTIONS = 1
   
    def __init__(self):
        self.serverRunning = True
        logging.basicConfig(level=logging.DEBUG)
    
    def get_available_ports(self, host, port_start, port_end):
        """!
        Get Available Ports 
        @param host String: host addr
        @param port_start Int: start port of range
        @param port_end Int: end port of range (included)
        @return Return list of port available.
        """
        available_ports = Utils.get_unused_ports(host, port_start, port_end+1)
        return available_ports

    def start_server(self, port_start, port_end, connections=CONNECTIONS):
        """!
        Start Server just before start
        @param port_start Int: start range of port
        @param port_end Int: end range onf port
        @param connections Int: Max numbers of connections (default 1)
        @return void:
        """

        # The server need to find where he CAN run, on wich port
        config = self.get_config()
        socketInterpreterSettings = config.get('socketInterpreterSettings', {})
        host = socketInterpreterSettings.get('host', {})
        available_ports = self.get_available_ports(host, port_start, port_end)
        
        if(len(available_ports) < 1) : return # if no port available

        # else, take the first or array
        threading.Thread(target=self.main_server, args=(host, available_ports[0], connections)).start()

    def start_with_config(self):
        """!
        To configure server before call startServer, depend on which dcc used
        """
        pass

    def get_config(self):
        """!
        Get Config from node server
        @return config file as data json
        """
        # Read json file
        with open(self.CONFIG_PATH) as config:
            data = json.load(config)

        return data
    # --- Override Part ---

    def function_to_process(self, data, client):
        """!
        Function to execute, received command (callback)
        @param data Json: Received Data
        @param client SocketClient: Client Connection
        """
        logging.error("function_to_process not implemented")
        
    
    def process_update(self, data, client):
        """!
        Redirect execution of data received (onMainThread for maya, for example)
        @param data Json: Received Data
        @param client SocketClient: Client Connection
        """
        logging.error("process_update not implemented")

    
    def on_shutdown(self):
        """!
        On Shutdown Action
        """
        self.serverRunning = False

    def on_restart(self):
        """!
        Route, to restart Server
        """
        time.sleep(.300)
        self.start_with_config()
        
    
    def on_identify_dcc(self, client):
        """!
        On Identify Dcc Action [Need to be override per dcc]
        @param client SocketClient: Client Connection
        """
        client.send("Idendity not implemented")

    # --- End Override Part ---
   

    # Generic method to start all server in python 2
    def main_server(self, host, port, connections):
        """!
        Main server entry point
        @param host String: Host ip running server
        @param port Number: Port running server
        @param connections Int: Number of connections to handle
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        try:
            sock.bind((host, port)) 
        except Exception as socket_error:
            msg = "Socket Server, Failed to open port: {}".format(socket_error)
            logging.error(msg)
            return

        sock.listen(connections)
        logging.info("REZ Starting Server: {}:{}".format(host, port))
        
        self.serverRunning = True
        while self.serverRunning:
            client, address = sock.accept()
            data = client.recv(1024)
            if data:
                if data == "#Shutdown#":
                    self.on_shutdown()

                if data == "#Identify#":
                    self.on_identify_dcc(client)

                if data == "#Restart#":
                    self.on_shutdown()

                else:
                    logging.info("Socket Server, Data Received: {}".format(data))
                    self.process_update(data, client)

            try:
                client.close()
            except Exception as client_error:
                logging.info("Socket Server, Error Closing Client Socket: {}".format(client_error))

        logging.info("Socket Server, Shutting Down.")

        try:
            sock.close()
        except Exception as close_error:
            logging.info("Socket Server, Error Closing Socket: {}".format(close_error))

        if data == "#Restart#":
            self.on_restart()