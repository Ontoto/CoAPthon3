from coapthon.client.helperclient import HelperClient
from datetime import datetime

host = "192.168.15.13"
port = 5683
path ="config?test"


# for i in range(0,1):
client = HelperClient(server=(host, port))

# print(i)
response = client.get(path)
print(response.pretty_print())
print("rx")
client.stop()
client = HelperClient(server=(host, port))
response = client.post(path,"null")
print(response.pretty_print())
client.stop()