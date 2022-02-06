import pycom
from network import Bluetooth

# Red led when disconnected BLE
pycom.heartbeat(False)
pycom.rgbled(0x7f0000)

# Connection/disconnection callback
def connection_ble(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
        pycom.rgbled(0x007f00) #green

    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")
        pycom.rgbled(0x7f0000) #red

# Write image callback
def receive_image_ble(chr, data):
    events, value = data
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request with value = {}".format(value))
    else:
        print('Read request on char 1')

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='imgoverlora', service_uuid=b'36c4919279684969')
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=connection_ble)
bluetooth.advertise(True)

service = bluetooth.service(uuid=b'ce397c4d744e41ab', isprimary=True)
char1 = service.characteristic(uuid=b'0242ac120002a8a3', value=5)
char1_callback = char1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=receive_image_ble)
