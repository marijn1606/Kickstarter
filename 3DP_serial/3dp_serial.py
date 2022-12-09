import serial as pyserial
import threading
import time

port = 'COM5'
baud = 115200
status = "ready"

serial = pyserial.Serial(port, baud, timeout=0)
time.sleep(5)


def send_command(command, send_sequence=False):
    serial.write(str.encode(command + "\r\n"))
    serial.write(str.encode("M400" + "\r\n"))
    global status
    status = "processing"


def serial_status():
    global status
    serial_data = ""
    while serial.inWaiting():
        serial_data = serial.readline().decode()
        # print(serial_data)
    if serial_data == "ok\n":
        status = "ready"
    return status


command_list = [
    # "G28",
    # "G92 X0 Y0 Z0",
    "G1 Z50 F1000",
    "G1 X100 F1000",
    "G1 X50 F1000",
    "G1 X100 F1000",
    "G1 X50 F5000",
    "G1 X100 F5000",
    "G1 X50 F5000",
    "G1 X100 F5000",
    "G1 X50 F5000",
    "G1 X100 F5000",
    "G1 X50 F5000",
    "G1 X100 F5000"
]

# while True:
for command in command_list:
    send_command(command)
    while serial_status() != "ready":
        print("waiting for printer")
        time.sleep(0.05)
    print("Completed")
