import random
import time
from adafruit import *
from timer import *
from uart import *

WRITE_TIMER = 0;

frequency = 10;
setTimer(0, 1);
setTimer(1, 1)

while True:
    timerRun()

    # if timerTimeout(1):
    #     setTimer(1, 3)
    #     temp = random.randint(0,100)
    #     humid = random.randint(0,100)
    #     print(temp," ",humid)
    #     client.publish("cambien1", temp)
    #     client.publish("cambien2", humid)
    
    
    frequency = getFreq();
    
    if timerTimeout(WRITE_TIMER):
        setTimer(WRITE_TIMER, frequency);
        writeSerial("READ");
        
    readSerial(client);
    
    time.sleep(1)