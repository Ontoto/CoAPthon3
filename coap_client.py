from coapthon.client.helperclient import HelperClient
from datetime import datetime
from coapthon import defines
import paho.mqtt.publish as publish
mqttAuth = {'username': 'Logger', 'password': 'Pa55w0rd@L0GgEr'}
host = "203.166.239.45"
port = 5683
path ="config?867997030018781"



# for i in range(0,1):
client = HelperClient(server=(host, port))
# a = bytearray(b'\xAF\x02\x00\x00')                
# publish.single("config/test/2", payload=a, qos=0, hostname="mqtt.ontoto.com.au", auth=mqttAuth,retain=True)
                #    
# print(i)
# ct = {'content_type': defines.Content_types["application/octet-stream"]}
response = client.get(path)
print(response.pretty_print())
print("rx")
client.stop()
client = HelperClient(server=(host, port))
response = client.post(path,b"\x22\x23\x00")
print(response.pretty_print())
print("rx")