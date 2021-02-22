#!/usr/bin/env python

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from traceback import print_exc

import logging
import re

from datetime import datetime
import time

mqttAuth = {'username': 'Logger', 'password': 'Pa55w0rd@L0GgEr'}

logging.basicConfig(filename='./tmp/error.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "test"

    def render_GET(self, request):
        print(request.pretty_print())
        subpaths = []
        for opt in request.options:
            print(str(opt))
            path = re.sub(r'\s+','',str(opt)).split(':')
            if path:
                subpaths.append(path[1])
        if len(subpaths) == 2:
            print(subpaths)
            # Valid path
            id = subpaths[1]
            print("Received message from:", id)
            topic = subpaths[0] + "/" + id
            print("Subscribing to topic:", topic)
            try:
                msg = subscribe.simple(topic, hostname="mqtt.ontoto.com", auth=mqttAuth)
                print("%s %s" % (msg.topic, msg.payload))
                self.payload = msg.payload                             
            except Exception as e:
                self.payload = "null"
                print("Exception occurred")
                print('type is:', e.__class__.__name__)
                print_exc()
                logger.error(e.__class__.__name__)  
        return self

    def render_PUT(self, request):
        self.payload = request.payload
        return self

    def render_POST(self, request):
        # print(request.pretty_print())
        # res.location_query = request.uri_query
        # res.payload = request.payload
        # print(len(request.uri_query))
        # print(request.uri_query)
        # print(res.payload)
        print(request.pretty_print())
        subpaths = []
        for opt in request.options:
            print(str(opt))
            path = re.sub(r'\s+','',str(opt)).split(':')
            if path:
                subpaths.append(path[1])
        if len(subpaths) == 2:
            print(subpaths)
            # Valid path
            id = subpaths[1]
            print("Received message from:", id) 
            timestamp = datetime.utcnow()
            topic = subpaths[0] + "/" + id
            if subpaths[0] == 'b':
                # Publishing data
                topic += timestamp.strftime('/%m/%d/%H/%M/%S')
            print("Publishing to topic:", topic)
            try:
                publish.single(topic, payload=request.payload, qos=0, hostname="mqtt.ontoto.com.au", auth=mqttAuth,
                                retain=True)               
            except Exception as e:
                print("Exception occurred")
                print('type is:', e.__class__.__name__)
                print_exc()
                logger.error(e.__class__.__name__)

        return True

    def render_DELETE(self, request):
        return True
    

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('b/', BasicResource())
        self.add_resource('config/', BasicResource())

def main():
    server = CoAPServer("192.168.15.13", 5683)
    try:
        server.listen(1)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    main()