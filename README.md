## Modbus Plugins for Domoticz
Author: Sebastiaan Ebeltjes / domoticx.nl

### Support for:
* RTU
* ASCII
* TCP

Succesfully Tested on Domoticz version: 3.8153 (Stable)

-----
### Using RTU / ASCII (SERIAL HW)

* Hardware: USB RS485-Serial Stick like **[This one](http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386)**
* Setup: Select method "RTU" or "ASCII", Serial Port, BaudRate, PortSettings
* Device adress is most likely: 1 to 247
* Payload in HEX, like: 0x0100

-----
### Using TCP

* Hardware: Not required
* Setup: Select method "TCP"
* Device adress is most likely an ip: xxx.xxx.xxx.xxx
* Payload in HEX, like: 0x0100

-----
### Functions of the WRITE plugin

* Write Single Coil (Function 5)
* Write Single Holding Register (Function 6)
* Write Multiple Coils (Function 15)
* Write Registers (Function 16)

-----
### Dependancies

For this plugin to work you need to install: **pymodbus**

Install for python 3.x with: ```sudo pip3 install -U pymodbus```

Preferred is v1.4.0 or higher!

-----
### HW Tested:
* [Relay board](http://domoticx.com/modbus-relaisbord/)
