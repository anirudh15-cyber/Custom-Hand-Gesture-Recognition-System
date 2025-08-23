from cvzone.SerialModule import SerialObject
from time import sleep

arduino = SerialObject()

while True:
    arduino.sendData([50])
