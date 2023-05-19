import serial.tools.list_ports
import sys

MCU_MAX_CONNECT_ATTEMP = 3;

connectTried = 0;

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        print(strPort)
        if "Silicon Labs CP210x USB to UART Bridge" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    #return "COM5"; #emulator port
   
def connectClient():
    portName = getPort();

    if portName != "None":
        # client.publish("cambien3", "MCU CONNECTED");
        ser = serial.Serial(port=portName, baudrate=9600)
        print(ser)
    else:
        print("NONE")
    return ser;

ser = connectClient();
   
mess = ""

def processData(data, client):
    data = data.replace("!", "")
    data = data.replace("#", "")
    global splitData
    splitData = data.split(":")
    print(splitData)
    if splitData[0]=='OK':
        currentTemp = float(splitData[1]);
        currentHumid = float(splitData[2]);
        if (currentTemp >= 5 and currentTemp <= 50):
            client.publish("cambien2", str(currentHumid));
            client.publish("cambien1", str(currentTemp));
        else:
            return;
    elif splitData[0]=='ERROR':
        client.publish("cambien3", "SENSOR ISSUE!");
    elif splitData[0] == 'VER':
        MCUver = splitData[1];
        MCUfirmwareVer = splitData[2];
        print(MCUver + MCUfirmwareVer);

def readSerial(client):
    if ser.port != "None":
        bytesToRead = ser.inWaiting()
        data = ""
        if (bytesToRead > 0):
            global mess
            mess = mess + ser.read(bytesToRead).decode("UTF-8")
            while ("#" in mess) and ("!" in mess):
                start = mess.find("!")
                end = mess.find("#")
                processData(mess[start:end + 1], client)
                if (end == len(mess)):
                    mess = ""
                else:
                    mess = mess[end + 1:]
    else:
        portName = getPort();
        if portName == "None":
            connectTried += 1;
            print("Attemp connect number", connectTried);
            if connectTried == MCU_MAX_CONNECT_ATTEMP:
                client.publish("cambien3", "MCU DISCONNECTED");
                print("MCU DISCONNECTED");
                connectTried = 0;
                sys.exit(1);

def writeSerial(value):
    if ser.port != "None":
        write_data = "!" + str(value) + "#"
        ser.write(write_data.encode());
