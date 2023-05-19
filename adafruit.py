from Adafruit_IO import MQTTClient
import sys
from uart import writeSerial

AIO_FEED_ID = ["nutnhan1","nutnhan2", "freq"]
AIO_USERNAME = "Rumin2k2"
AIO_KEY = "aio_PcJj10KjmtoSyJdD5gYsGNmVX8xI"

frequency = 10;

def getFreq():
    return frequency;

def connected(client):
    print("Ket noi thanh cong ...")
    for id in AIO_FEED_ID:
        client.subscribe(id)
    client.publish("freq", str(frequency));

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client , feed_id , payload):
    global frequency;
    print("Data from " + feed_id + ":" + payload)
    if feed_id == "nutnhan1":
        if payload == '0':
            writeSerial("OFF1");
        else:
            writeSerial("ON1");
    if feed_id == "nutnhan2":
        if payload == '0':
            writeSerial("OFF2")
        else:
            writeSerial("ON2");
    if feed_id == "freq":
        frequency = int(payload);

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
