# EITN30F-LoRa
Internet Inside PhD-course at LTH. Followed course spring 2021.

# SPI (on the RPi 4B)
To enable edit
```sh
sudo vi /boot/config.txt
```
and make sure the following lines exist. The second line enables SPI bus 1.
```
dtparam=spi=on
dtoverlay=spi1-1cs
```
Reboot the RPi and check that SPI is enabled
```sh
ls -l /dev/spidev*
```
should output
```sh
/dev/spidev0.0  /dev/spidev0.1  /dev/spidev1.0
```

# Ansible
Install ansible on the "control" laptop. And make sure the key to SSH is copied to the hosts.
```sh
pip3 install --user ansible
```
Then if the hosts are online you should be able to ping both at the same time with (if not executed from the _ansible-files_ folder, the full path to the inventory needs to be specified.
```sh
ansible -i inventory all -m ping
```

Now we can install the Adafruit python3 packages on all hosts (in the inventory file) with the following command assuming that you have the same sudo password on all hosts.
```
ansible-playbook -i inventory MyAnsiblePlays.yml -K
```

# Applications/Packages/Dependencies
```sh
sudo pip3 install adafruit-blinka adafruit-circuitpython-rfm9x adafruit-circuitpython-busdevice
```
To get a nice prinout in the terminal with information about the board and the GPIO layout, install
```sh
sudo apt install python3-gpiozero
```
and run
```sh
pinout
```
which should display something similar to
```sh
´--------------------------------.
| oooooooooooooooooooo J8   +======
| 1ooooooooooooooooooo  PoE |   Net
|  Wi                    oo +======
|  Fi  Pi Model 4B  V1.2 oo      |
|        ,----.               +====
| |D|    |SoC |               |USB3
| |S|    |    |               +====
| |I|    `----'                  |
|                   |C|       +====
|                   |S|       |USB2
| pwr   |HD|   |HD| |I||A|    +====
`-| |---|MI|---|MI|----|V|-------'

Revision           : c03112
SoC                : BCM2711
RAM                : 4096Mb
Storage            : MicroSD
USB ports          : 4 (excluding power)
Ethernet ports     : 1
Wi-fi              : True
Bluetooth          : True
Camera ports (CSI) : 1
Display ports (DSI): 1

J8:
   3V3  (1) (2)  5V    
 GPIO2  (3) (4)  5V    
 GPIO3  (5) (6)  GND   
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND   
GPIO22 (15) (16) GPIO23
   3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND   
 GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8 
   GND (25) (26) GPIO7 
 GPIO0 (27) (28) GPIO1 
 GPIO5 (29) (30) GND   
 GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND   
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
   GND (39) (40) GPIO21

For further information, please refer to https://pinout.xyz/
```
