# boot.py -- run on boot-up
import machine, UART
import os
from network import WLAN

# Enable UART
uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('sender.py')

# Disable Wi-Fi
wlan = WLAN()
wlan.deinit()