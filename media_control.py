#!/usr/bin/env python
import serial
import signal
import sys
import glob
import time
import os

class VolumeControl:

    def __init__(self):

        self.serial = None
        self.running = True
        self.resolution = 2**10
        self.interrupt_called = 0

    def set_volume(self, val):
        if val == -10:
            os.system("amixer -q -D pulse sset Master toggle")
        elif val == -20:
            os.system("playerctl -p chrome play-pause")
        elif val == -30:
            os.system("playerctl -p chrome next")
        elif val == -40:
            os.system("playerctl -p chrome previous")
        else:
            percentage = round(100*(val / self.resolution))
            os.system("amixer -q -D pulse sset Master %d%%"%(percentage))

    def validate_connection(self):
        # TODO: Implement
        return True

    def connect_serial(self):
        
        print("Trying to connect...")
        while True:
            for device_name in glob.glob("/dev/ttyACM*"):
                try:
                    self.serial = serial.Serial(device_name, timeout=1)  # open serial port
                except:
                    continue
                if not self.validate_connection():
                    self.serial = None
                else:
                    print("Serial connection opened.")
                    return
            
            time.sleep(2)

    def run(self):
        
        self.connect_serial()

        while self.running:
            try:
                line = self.serial.readline()
            except serial.serialutil.SerialException:
                # Recover if the connection is broken until the program is manually terminated.
                self.serial = None
                print("Connection broken.")
                while self.running and self.serial is None:
                    self.connect_serial()

            if len(line) == 0:
                continue
            val = int(line.decode().strip())
            self.set_volume(val)

        self.serial.close()
        print("Serial connection closed.")

    def signal_handler(self, *args):
        print("Interrupt called.")
        self.running = False
        self.interrupt_called += 1

        # Force quit
        if self.interrupt_called > 2:
            sys.exit(0)

def main():

    vc = VolumeControl()
    signal.signal(signal.SIGINT, vc.signal_handler)

    vc.run()

if __name__ == "__main__":
    main()
