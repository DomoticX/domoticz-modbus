### Modbus Read/Write Plugins for Domoticz
Author: Sebastiaan Ebeltjes / domoticx.nl

**Support for:

* RS232/RS485
* RTU
* ASCII
* RTU over TCP
* TCP/IP

**Functions of the READ plugin**

* Read Coil (Function 1)
* Read Discrete Input (Function 2)
* Read Holding Registers (Function 3)
* Read Input Registers (Function 4)

Supported data types:

* No conversion (passtrough)
* INT 8/16/32/64-Bit
* UINT 8/16/32/64-Bit
* FLOAT 32/64-Bit

**Functions of the WRITE plugin**

* Write Single Coil (Function 5)
* Write Single Holding Register (Function 6)
* Write Multiple Coils (Function 15)
* Write Registers (Function 16)

RTU/ASCII/RTU over TCP: Write HEX Payloads, like: 0x0100
TCP/IP: Write INT Payloads, like: 53

-----
### Installation

Place the folders inside the domoticz plugin folder, for example like this construction:

**/home/pi/domoticz/plugins/modbus-write/plugin.py**

**/home/pi/domoticz/plugins/modbus-read/plugin.py**

Then restart domoticz with: ```sudo service domoticz.sh restart```

Succesfully Tested on Domoticz version: 3.8153 (Stable)

-----
### Using RTU / ASCII (SERIAL HW)

* Hardware: USB RS485-Serial Stick like **[This one](http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386)**
* Setup: Select method "RTU" or "ASCII", Serial Port, BaudRate, PortSettings
* Device adress is most likely: 1 to 247
* Payload in HEX, like: 0x0100

-----
### Using RTU over TCP / TCP/IP

* Hardware: Not required
* Setup: Select method "TCP"
* Device adress is most likely an ip: xxx.xxx.xxx.xxx
* Payload in HEX, like: 0x0100

-----
### Dependancies

For this plugin to work you need to install some dependancies

**pymodbus AND pymodbusTCP**

Install for python 3.x with: ```sudo pip3 install -U pymodbus pymodbusTCP```

**six**

Six is a Python 2 and 3 compatibility library. It provides utility functions for smoothing over the differences between the Python versions with the goal of writing Python code that is compatible on both Python versions.

1) Install for python 3.x with: ```sudo pip3 install -U six```

(will install in /home/pi/.local/lib/python2.7/site-packages/)

2) copy the py file to v3.x python

```sudo cp six.py /usr/lib/python3.4```

or

```sudo cp six.py /usr/lib/python3.5```

-----
### HW Tested:
* [Relay board](http://domoticx.com/modbus-relaisbord/)
* [KWh Meter - EASTRON SDM120](http://domoticx.com/modbus-kwh-meter-eastron-sdm120/)
