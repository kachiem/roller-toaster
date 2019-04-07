import serial
import time

BAUD_RATE = 115200
PORT = "/dev/tty.7-DevB"

TIMEOUT = 2

# Bytes!
FORWARD = b"w"
BACKWARD = b"s"
LEFT = b"a"
RIGHT = b"d"
SERVO_LEFT = b"q"
SERVO_RIGHT = b"e"

def forward():
    bt.write(FORWARD)
    time.sleep(TIMEOUT)

def backwards():
    bt.write(BACKWARD)
    time.sleep(TIMEOUT)

def left():
    bt.write(LEFT)
    time.sleep(TIMEOUT)

def right():
    bt.write(RIGHT)
    time.sleep(TIMEOUT)

def servo_left():
    bt.write(SERVO_LEFT)
    time.sleep(TIMEOUT)

def servo_right():
    bt.write(SERVO_RIGHT)
    time.sleep(TIMEOUT)

# Setup serial port with path to port
bt = serial.Serial(PORT, 115200, timeout=5)
bt.flushInput()

while True:
    cmd = input('Enter your command: ')
    if cmd == 'w':
        forward()
    elif cmd == 'a':
        left()
    elif cmd == 's':
        backwards()
    elif cmd == 'd':
        right()
    elif cmd == 'q':
        servo_left()
    elif cmd == 'e':
        servo_right()
    else:
        exit()