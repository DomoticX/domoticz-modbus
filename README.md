## Modbus Plugins for Domoticz
Author: Sebastiaan Ebeltjes / domoticx.nl

### Support for:
* RTU
* ASCII
* TCP
-----
### Using Serial HW (RTU / ASCII)
Hardware: USB RS485-Serial Stick like **[This one](http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386)**
Setup
-----
### Functions WRITE plugin
* Write Single Coil (Function 5)
* Write Single Holding Register (Function 6)
* Write Multiple Coils (Function 15)
* Write Registers (Function 16)
-----
### Dependancies
For this plugin to work you need to install: **pymodbus3**

Install for python 3 with: ```sudo pip3 install -U pymodbus3```
-----
### HW Tested:
* [Relay board](http://domoticx.com/modbus-relaisbord/)
