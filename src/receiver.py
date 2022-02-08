import pycom
import loractp
import time

# LED status indicator 
lora_connected = False

# LoRa directions
myaddr = ""
rcvraddr = ""

# Update led status indicator
def update_status():
    if lora_connected:
        pycom.rgbled(0x007f00) #red
    else:
        pycom.rgbled(0x7f0000) #red

ctpc = loractp.CTPendpoint()

status = -1
number_of_messages = 0
update_status()

while (status == -1):
    myaddr, rcvraddr, status = ctpc.listen()

    if (status == 0):
        print("Reciever: LoRa connection from {} to me ({})".format(rcvraddr, myaddr))
        lora_connected = True

    else:
        print("Reciever: Failed LoRa connection from {} to me ({})".format(rcvraddr, myaddr))
        lora_connected = False

    update_status()
    time.sleep(5)

while True:
    try:
        rcvd_data, addr = ctpc.recvit()
        print("Reciever: From {} got {}".format(addr, rcvd_data))

        time.sleep(20)
    except Exception as e:
        print ("Reciever: EXCEPTION!! ", e)
        break