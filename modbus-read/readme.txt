Changelog:
v1.2.1
 - Fixed the exception "Modbus Error: [Invalid Parameter] Invalid collection of registers supplied" on my Raspberry/Domoticz

v1.2.0
- Fixed TAB error.

v1.1.9
- Fixed debug output [Sandolution]

v1.1.8
- Added "sys.path.append('/usr/local/lib/python3.5/dist-packages')" in the begining for modern python libraries compatibility. [akliouev]
- After wrestling for a day finaly found out that "data" is a list and doesn't have method ".registers" associated with it. [akliouev]
  Must be remnants of older pymodbus versions. Changed "data.registers" -> "data". [akliouev]
- Fix: line 403 was verifying that Username is "1" (only "read coil") and otherwise wasn't updating anything. [akliouev]

v1.1.7
- Removed debug option due to implementation of sensor type. [Sandolution]
- Added more options for data type (swapping of low/high byte/word). [Sandolution]
- Adjusted dividing settings to include 10000. [Sandolution]
- Added more append paths [Sandolution]

v1.1.6
- Added import RTU framer for RTU over TCP to work. [Sandolution]
- Fix for unit id on RTU over TCP [Sandolution]

v1.1.5
- Added ID option for IP/TCP addresses. [S. Ebeltjes]

v1.1.4
- Removed debug option due to implementation of sensor type. [Sandolution]
- Added more options for data type (swapping of low/high byte/word). [Sandolution]
- Adjusted dividing settings to include 10000. [Sandolution]

TODO: float decode word orders
float AB CD == byteorder=Endian.Big, wordorder=Endian.Big
float CD AB == byteorder=Endian.Big, wordorder=Endian.Little
float BA DC == byteorder=Endian.Little, wordorder=Endian.Big
float DC BA == byteorder=Endian.Little, wordorder=Endian.Little
