import pyfirmata, time

board = pyfirmata.Arduino('/dev/cu.usbmodem14401')

while True:
    board.digital[3].write(1)
    time.sleep(1.0)
    board.digital[3].write(0)
    time.sleep(100.0)