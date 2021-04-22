import serial
import time


def getTemperature():
    s = serial.Serial('COM3')
    while True:
        res = s.readline().decode("utf-8").rstrip()
        print(res)