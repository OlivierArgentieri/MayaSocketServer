from src.servers.base.base_socketserver import BaseSocketServer

import maya.cmds as cmds
import maya.utils as maya_utils

import sys
import logging
import socket
import threading
import json

##########################################################
# class server for mayapy. inherit BaseSocketServer class
##########################################################
class MayapySocketServer(BaseSocketServer):

    def __init__(self):
        super(MayapySocketServer, self).__init__()
        logging.basicConfig(level=logging.DEBUG)
        
        self.start_with_config()
    
    def start_with_config(self):
        """!
        To configure server before call startServer, depend on which dcc used
        """
        config = self.get_config()

        port_start = config.get('dccPortSettings', {}).get('mayaPortRangeStart', 0)
        port_end = config.get('dccPortSettings', {}).get('mayaPortRangeEnd', 0)
        
        sys.path.append(config.get('pipelineSettings', {}).get('mayapyActionsPath', 0)) # add houdini action in sys path 
        self.start_server(port_start, port_end, self.CONNECTIONS)

    def function_to_process(self, data, client):
        """!
        Function to execute, received command (callback)
        @param data Json: Received Data
        @param client SocketClient: Client Connection
        """

        logging.info("Mayapy Server, Process Function: {}".format(data))

        out = ""
        if("print" in data):
            data = data.replace("print", "out = str")

        try:
            cmds.headsUpMessage("Processing incoming data: {}".format(data), time=3.0)
            exec(data)
            client.send(out)
        except Exception as exec_error:
            client.send(str(exec_error))

    def process_update(self, data, client):
        """!
        Process incoming data, run this in the Maya main thread
        @param data Json: Received Data
        @param client SocketClient: Client Connection
        """
        
        try:
            self.function_to_process(data, client)
        except Exception as e:
            cmds.error("Mayapy Server, Exception processing Function: {}".format(e))
    
    def on_identify_dcc(self, client):
        """!
        On Identify Dcc Action
        @param client SocketClient: Client Connection
        """

        name = 'unsaved'
        exec_name = sys.executable.rsplit('\\',1)[1]
        exec_name = exec_name.split('.')[0]
        data ="print(json.dumps({'filename': '" + name + "', 'exec_name': '" + exec_name + "'}, sort_keys=True, indent=4))"
        self.function_to_process(data, client)

    def on_shutdown(self):
        """!
        On Shutdown Action
        """
        self.serverRunning = False
        sys.exit()