from network import Bluetooth
import loractp
import pycom
import gc
import time
import ujson

# LED status indicator 
ble_connected = False
lora_connected = False

# Data to recieve over BLE
data_to_send = b''

# LoRa directions
myaddr = ""
rcvraddr = ""

# Update led status indicator
def update_status(ble_connected=None):
    if not ble_connected and not lora_connected:
        pycom.rgbled(0x7f0000) #red

    if not ble_connected and lora_connected:
        pycom.rgbled(0x0000FF) #blue

    if ble_connected and lora_connected:
        pycom.rgbled(0x007f00) #green

    if ble_connected and not lora_connected:
        pycom.rgbled(0xFFFF00) #yellow

# Connection/disconnection callback
def connection_ble(bt_o):
    events = bt_o.events()
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Sender: BLE connected")
        update_status(True)

    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Sender: BLE disconnected")
        update_status(False)

def save_data_to_send(data):
    global data_to_send
    if (data != None):
        data_to_send += data
    else:
        data_to_send = b''

# Write image callback
def receive_image_ble(chr, data):
    events, value = data
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Sender: Write request with value = {}".format(value))
        save_data_to_send(value)

def send_image_lora(chr, data):
    events, value = data
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print(value)
        if value == b'send':
            t0 = time.time()
            addr, quality, result = ctpc.sendit(rcvraddr, data_to_send)
            t1 = time.time()
            timetosend = t1-t0
            print("Sender: ACK from {} (time = {:.4f} seconds, quality = {}, result {})".format(addr, timetosend, quality, result))
            save_data_to_send(None)

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='LoPy-IMGoverLora', service_uuid=b'36c4919279684969')
bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=connection_ble)
bluetooth.advertise(True)

service = bluetooth.service(uuid=b'ce397c4d744e41ab', isprimary=True, nbr_chars=2)
char1 = service.characteristic(uuid=b'0242ac120002a8a3')
char1_callback = char1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=receive_image_ble)

char2 = service.characteristic(uuid=b'0f18b91b2afc3e3d')
char2_callback = char2.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=send_image_lora)

# Enable garbage collector 
gc.enable()

# Create loractp endpoint
ctpc = loractp.CTPendpoint()

# Connect to node B
status = -1
update_status()

while (status == -1):
    myaddr, rcvraddr, quality, status = ctpc.connect()

    if (status == 0):
        print("Sender: LoRa connection from {} to me ({})".format(rcvraddr, myaddr))
        lora_connected = True

    else:
        print("Sender: Failed LoRa connection from {} to me ({})".format(rcvraddr, myaddr))
        lora_connected = False

    update_status()
    time.sleep(5)