import os
import time
import threading
import board
import neopixel

neo = neopixel.NeoPixel(board.D18, 8)
BT_SERIAL_PATH = '/dev/rfcomm0'
red = 0
green = 0
blue = 0

def _bluetoothProcess():
    while True:
        try:
            with open(BT_SERIAL_PATH, 'r') as rf:
                line = rf.readline()
                if not line:
                    print('Bluetooth Disconnected')
                    time.sleep(2)
                    break
                line = line.split(',')
                red = int(line[0])
                green = int(line[1])
                blue = int(line[2])
                res = int(line[3])
                print('recv : ', red, green, blue, res)
                neo.fill((red,green,blue))
                neo.show()
        except Exception as e:
            print(e)
            time.sleep(2)

def bluetoothThreadStart():
    btThread = threading.Thread(target=_bluetoothProcess, args=())
    btThread.start()


if __name__ == '__main__':
#    bluetoothThreadStart()
    _bluetoothProcess()