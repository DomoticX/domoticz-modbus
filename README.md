### Modbus Read/Write Plugins for Domoticz
Author: Sebastiaan Ebeltjes / DomoticX.nl

Succesfully Tested on Domoticz version: 2020.2

**Support for:**

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
* BOOL (TRUE/FALSE)
* INT 8/16/32/64-Bit
* UINT 8/16/32/64-Bit
* FLOAT 32/64-Bit
* STRING 2/4/6/8 Bytes

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

-----
### Using RTU / ASCII (SERIAL HW)

* Hardware: USB RS485-Serial Stick like **[This one](http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386)**
* Setup: Select method "RTU" or "ASCII", Serial Port, BaudRate, PortSettings
* Device adress is most likely: 1 to 247
* Payload in HEX, like: 0x0100

-----
### Using RTU over TCP / TCP/IP

* Hardware: Not required
* Setup: Select method "RTU over TCP" or "TCP/IP"
* Device adress is most likely an ip: xxx.xxx.xxx.xxx
* Port is default 502
* RTU over TCP: Write HEX Payloads, like: 0x0100
* TCP/IP: Write INT Payloads, like: 53

-----
### Dependancies

Raspbian iamge (FULL version recommended)
For this plugin to work you need to install some python3 dependancies:

**pymodbus AND pymodbusTCP**

Install with: ```sudo pip3 install -U pymodbus pymodbusTCP```

-----
### HW Tested:
* [Relay board](http://domoticx.com/modbus-relaisbord/)
* [KWh Meter - EASTRON SDM120](http://domoticx.com/modbus-kwh-meter-eastron-sdm120/)
* [Temp/Hum sensor - XY-MD01 or XY-MD02](http://domoticx.com/modbus-temp-hum-sensor-xy-md02/)