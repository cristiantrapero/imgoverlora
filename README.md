# IMGoverLoRa: Send images over LoRA with BLE and Android

This project allows to transfer images over a LoRa (pure LoRa, no LoRaWAN) channel. This is implemented for the Pycom Lopy 4. The lopy deploys a BLE server to contact the Android application that will send the image. Once received, it is forwarded by LoRa to another Lopy 4.

# How to deploy the application
1. Install NojeJS depending on the operating system you are using: https://nodejs.org/es/download/
2. Install the Pymakr environment for VSCode as described here: https://docs.pycom.io/gettingstarted/software/vscode/
3. Clone this repository: `git clone https://github.com/cristiantrapero/imgoverlora.git`
4. Open this project in VSCode
5. Connect the Lopy 4 to the computer USB
6. List the serial ports with the Pymakr bar: `All commands -> Pymakr -> Extra -> List Serial Ports`
7. Change the `"address": "COM5"` in the pymakr.conf file to your corresponding setial port listed
8. Run the Pymakr command: `Upload`
9. Wait until load the project in the Lopy 4
10. Open the `receiver.py` file in the VSCode editor and select `Run` in the Pymakr bar
11. **Repeat the process for the other Lopy** from the point 4 until the 9 and then select the `sender.py` file in the VSCode editor and select `Run` in the Pymakr bar
12. All Lopy nodes are ready to work. If everything went well, you will have one terminal open for each Lopy node, and the light on the receiving node will be green ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) and the light on the sending node will be blue ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) (waiting for a BLE connection).

# Files
The repository is structured as follow:

- `src`: Contains the source code of the project concerning the implementation of the sender and receiver.
  - boot.py: Disables WiFi to avoid interferences
  - sender.py: Sender node code (Node A)
  - reciever.py: Reciever node code (Node B)
- `lib`: LoRaCTP protocol library.
  - loractp.py: Contains the lora content transfer protocol with his API
- `pymakr.conf`: Pymakr configuration file. **Is necessary change `"address": "COM5"` setting**.

## Firmware versions
Lopy4 firmware version: 
- Pycom MicroPython: **1.20.2.r6 [v1.11-c5a0a97]** released at 2021-10-28.
- Pybytes Version: **1.7.1**

Pysense v1.0 firmware version: 
- DFU version: **0.0.8** available at https://docs.pycom.io/updatefirmware/expansionboard/


