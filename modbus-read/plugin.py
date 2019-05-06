# Modbus RTU/ASCII/TCP - Universal READ Plugin for Domoticz
#
# Author: Sebastiaan Ebeltjes / domoticx.nl
# Serial HW: USB RS485-Serial Stick, like: http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386
#
# Dependancies:
# - pymodbus AND pymodbusTCP:
#   - Install for python 3.x with: sudo pip3 install -U pymodbus pymodbusTCP
#
# - For Synology NAS DSM you may need to install these dependencies for python3:
#   - sudo pip3 install -U pymodbus constants
#   - sudo pip3 install -U pymodbus payload
#   - sudo pip3 install -U pymodbus serial

# NOTE: Some "name" fields are abused to put in more options ;-)
#
"""
<plugin key="Modbus" name="Modbus RTU/ASCII/TCP - READ v1.2.0" author="S. Ebeltjes / domoticx.nl" version="1.2.0" externallink="" wikilink="https://github.com/DomoticX/domoticz-modbus/">
    <params>
        <param field="Mode1" label="Method" width="120px" required="true">
            <options>
                <option label="RTU" value="rtu" default="true"/>
                <option label="ASCII" value="ascii"/>
                <option label="RTU over TCP" value="rtutcp"/>
                <option label="TCP/IP" value="tcpip"/>
            </options>
        </param>
        <param field="SerialPort" label="Serial Port" width="120px" required="true"/>
        <param field="Mode2" label="Baudrate" width="70px" required="true">
            <options>
                <option label="1200" value="1200"/>
                <option label="2400" value="2400"/>
                <option label="4800" value="4800"/>
                <option label="9600" value="9600" default="true"/>
                <option label="14400" value="14400"/>
                <option label="19200" value="19200"/>
                <option label="38400" value="38400"/>
                <option label="57600" value="57600"/>
                <option label="115200" value="115200"/>
            </options>
        </param>
        <param field="Mode3" label="Port settings" width="260px" required="true">
            <options>
                <option label="StopBits 1 / ByteSize 7 / Parity: None" value="S1B7PN"/>
                <option label="StopBits 1 / ByteSize 7 / Parity: Even" value="S1B7PE"/>
                <option label="StopBits 1 / ByteSize 7 / Parity: Odd" value="S1B7PO"/>
                <option label="StopBits 1 / ByteSize 8 / Parity: None" value="S1B8PN" default="true"/>
                <option label="StopBits 1 / ByteSize 8 / Parity: Even" value="S1B8PE"/>
                <option label="StopBits 1 / ByteSize 8 / Parity: Odd" value="S1B8PO"/>
                <option label="StopBits 2 / ByteSize 7 / Parity: None" value="S2B7PN"/>
                <option label="StopBits 2 / ByteSize 7 / Parity: Even" value="S2B7PE"/>
                <option label="StopBits 2 / ByteSize 7 / Parity: Odd" value="S2B7PO"/>
                <option label="StopBits 2 / ByteSize 8 / Parity: None" value="S2B8PN"/>
                <option label="StopBits 2 / ByteSize 8 / Parity: Even" value="S2B8PE"/>
                <option label="StopBits 2 / ByteSize 8 / Parity: Odd" value="S2B8PO"/>
            </options>
        </param>
        <param field="Address" label="Device address /ID(TCP)" width="120px" required="true"/>
        <param field="Port" label="Port (TCP)" value="502" width="75px"/>
        <param field="Username" label="Modbus Function" width="280px" required="true">
            <options>
                <option label="Read Coil (Function 1)" value="1"/>
                <option label="Read Discrete Input (Function 2)" value="2"/>
                <option label="Read Holding Registers (Function 3)" value="3"/>
                <option label="Read Input Registers (Function 4)" value="4" default="true"/>
            </options>
        </param>
        <param field="Password" label="Register number" width="75px" required="true"/>
        <param field="Mode6" label="Data type" width="180px" required="true">
            <options>
                <option label="No conversion (1 register)" value="noco"/>
                <option label="INT 8-Bit LSB" value="int8LSB"/>
                <option label="INT 8-Bit MSB" value="int8MSB"/>
                <option label="INT 16-Bit" value="int16"/>
                <option label="INT 16-Bit Swapped" value="int16s"/>
                <option label="INT 32-Bit" value="int32"/>
                <option label="INT 32-Bit Swapped" value="int32s"/>
                <option label="INT 64-Bit" value="int64"/>
                <option label="INT 64-Bit Swapped" value="int64s"/>
                <option label="UINT 8-Bit LSB" value="uint8LSB"/>
                <option label="UINT 8-Bit MSB" value="uint8MSB"/>
                <option label="UINT 16-Bit" value="uint16" default="true"/>
                <option label="UINT 16-Bit Swapped" value="uint16s"/>
                <option label="UINT 32-Bit" value="uint32"/>
                <option label="UINT 32-Bit Swapped" value="uint32s"/>
                <option label="UINT 64-Bit" value="uint64"/>
                <option label="UINT 64-Bit Swapped" value="uint64s"/>
                <option label="FLOAT 32-Bit" value="float32"/>
                <option label="FLOAT 32-Bit Swapped" value="float32"/>
                <option label="FLOAT 64-Bit" value="float64"/>
                <option label="FLOAT 64-Bit Swapped" value="float64s"/>
                <option label="STRING 2-byte" value="string2"/>
                <option label="STRING 4-byte" value="string4"/>
                <option label="STRING 6-byte" value="string6"/>
                <option label="STRING 8-byte" value="string8"/>
            </options>
        </param>
        <param field="Mode5" label="Divide value" width="100px" required="true">
            <options>
                <option label="No" value="div0" default="true"/>
                <option label="Divide /10" value="div10"/>
                <option label="Divide /100" value="div100"/>
                <option label="Divide /1000" value="div1000"/>
                <option label="Divide /10000" value="div10000"/>
            </options>
        </param>
	<param field="Mode4" label="Sensor type" width="180px" required="true" value="Custom">
            <options>
                <option label="Air Quality" value="Air Quality"/>
                <option label="Alert" value="Alert"/>
                <option label="Barometer" value="Barometer"/>
                <option label="Counter Incremental" value="Counter Incremental"/>
                <option label="Current/Ampere" value="Current/Ampere"/>
                <option label="Current (Single)" value="Current (Single)"/>
                <option label="Custom" value="Custom" default="true"/>
                <option label="Distance" value="Distance"/>
                <option label="Gas" value="Gas"/>
                <option label="Humidity" value="Humidity"/>
                <option label="Illumination" value="Illumination"/>
                <option label="kWh" value="kWh"/>
                <option label="Leaf Wetness" value="Leaf Wetness"/>
                <option label="Percentage" value="Percentage"/>
                <option label="Pressure" value="Pressure"/>
                <option label="Rain" value="Rain"/>
                <option label="Selector Switch" value="Selector Switch"/>
                <option label="Soil Moisture" value="Soil Moisture"/>
                <option label="Solar Radiation" value="Solar Radiation"/>
                <option label="Sound Level" value="Sound Level"/>
                <option label="Switch" value="Switch"/>
                <option label="Temperature" value="Temperature"/>
                <option label="Temp+Hum" value="Temp+Hum"/>
                <option label="Temp+Hum+Baro" value="Temp+Hum+Baro"/>
                <option label="Text" value="Text"/>
                <option label="Usage" value="Usage"/>
                <option label="UV" value="UV"/>
                <option label="Visibility" value="Visibility"/>
                <option label="Voltage" value="Voltage"/>
                <option label="Waterflow" value="Waterflow"/>
                <option label="Wind" value="Wind"/>
                <option label="Wind+Temp+Chill" value="Wind+Temp+Chill"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

import sys
# Raspberry Pi
sys.path.append('/usr/local/lib/python3.4/dist-packages')
sys.path.append('/usr/local/lib/python3.5/dist-packages')
sys.path.append('/usr/local/lib/python3.6/dist-packages')

# Synology NAS DSM 6.2 python 3.5.1
#sys.path.append('/usr/local/lib/python3.5/site-packages')
#sys.path.append('/volume1/@appstore/py3k/usr/local/lib/python3.5/site-packages')

# Windows 10 Python 3.5.1
#sys.path.append("C:/Users/USER_NAME/AppData/Local/Programs/Python/Python37/Lib/site-packages"

# RTU
from pymodbus.client.sync import ModbusSerialClient

# RTU over TCP
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer

# TCP/IP
from pyModbusTCP.client import ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# Declare internal variables
result = ""
value = 0
ignored = 0
data = []

class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        #if Parameters["Mode4"] == "debug": Domoticz.Debugging(1)
        Domoticz.Debugging(0)	#Enable debugging by default, mode 4 is used for sensor mode
        Domoticz.Log("Sensor Type: "+Parameters["Mode4"])
        #Removed the full name parameter
        #Due to the lack of more parameter posibility, the name will be the hardware name
        if (len(Devices) == 0): Domoticz.Device(Name=" ",  Unit=1, TypeName=Parameters["Mode4"], Image=0, Used=1).Create() #Added sensor type
        DumpConfigToLog()
        Domoticz.Log("Modbus RTU/ASCII/TCP - Universal READ loaded.")
        return

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")
        return

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        #Domoticz.Log("onHeartbeat called")

        # Wich serial port settings to use?
        if (Parameters["Mode3"] == "S1B7PN"): StopBits, ByteSize, Parity = 1, 7, "N"
        if (Parameters["Mode3"] == "S1B7PE"): StopBits, ByteSize, Parity = 1, 7, "E"
        if (Parameters["Mode3"] == "S1B7PO"): StopBits, ByteSize, Parity = 1, 7, "O"
        if (Parameters["Mode3"] == "S1B8PN"): StopBits, ByteSize, Parity = 1, 8, "N"
        if (Parameters["Mode3"] == "S1B8PE"): StopBits, ByteSize, Parity = 1, 8, "E"
        if (Parameters["Mode3"] == "S1B8PO"): StopBits, ByteSize, Parity = 1, 8, "O"
        if (Parameters["Mode3"] == "S2B7PN"): StopBits, ByteSize, Parity = 2, 7, "N"
        if (Parameters["Mode3"] == "S2B7PE"): StopBits, ByteSize, Parity = 2, 7, "E"
        if (Parameters["Mode3"] == "S2B7PO"): StopBits, ByteSize, Parity = 2, 7, "O"
        if (Parameters["Mode3"] == "S2B8PN"): StopBits, ByteSize, Parity = 2, 8, "N"
        if (Parameters["Mode3"] == "S2B8PE"): StopBits, ByteSize, Parity = 2, 8, "E"
        if (Parameters["Mode3"] == "S2B8PO"): StopBits, ByteSize, Parity = 2, 8, "O"

        # How many registers to read (depending on data type)?
	    # Added additional options for byte/word swapping
        registercount = 1 # Default
        if (Parameters["Mode6"] == "noco"): registercount = 1
        if (Parameters["Mode6"] == "int8LSB"): registercount = 1
        if (Parameters["Mode6"] == "int8MSB"): registercount = 1
        if (Parameters["Mode6"] == "int16"): registercount = 1
        if (Parameters["Mode6"] == "int16s"): registercount = 1
        if (Parameters["Mode6"] == "int32"): registercount = 2
        if (Parameters["Mode6"] == "int32s"): registercount = 2
        if (Parameters["Mode6"] == "int64"): registercount = 4
        if (Parameters["Mode6"] == "int64s"): registercount = 4
        if (Parameters["Mode6"] == "uint8LSB"): registercount = 1
        if (Parameters["Mode6"] == "uint8MSB"): registercount = 1
        if (Parameters["Mode6"] == "uint16"): registercount = 1
        if (Parameters["Mode6"] == "uint16s"): registercount = 1
        if (Parameters["Mode6"] == "uint32"): registercount = 2
        if (Parameters["Mode6"] == "uint32s"): registercount = 2
        if (Parameters["Mode6"] == "uint64"): registercount = 4
        if (Parameters["Mode6"] == "uint64s"): registercount = 4
        if (Parameters["Mode6"] == "float32"): registercount = 2
        if (Parameters["Mode6"] == "float32s"): registercount = 2
        if (Parameters["Mode6"] == "float64"): registercount = 4
        if (Parameters["Mode6"] == "float64s"): registercount = 4
        if (Parameters["Mode6"] == "string2"): registercount = 2
        if (Parameters["Mode6"] == "string4"): registercount = 4
        if (Parameters["Mode6"] == "string6"): registercount = 6
        if (Parameters["Mode6"] == "string8"): registercount = 8

        # Split address to support TCP/IP device ID
        AddressData = Parameters["Address"].split("/") # Split on "/"
        UnitAddress = AddressData[0]

        # Is there a unit ID given after the IP? (e.g. 192.168.2.100/56)
        UnitIdForIp = 1 # Default
        if len(AddressData) > 1:
          UnitIdForIp = AddressData[1]

        ###################################
        # pymodbus: RTU / ASCII
        ###################################
        if (Parameters["Mode1"] == "rtu" or Parameters["Mode1"] == "ascii"):
          Domoticz.Debug("MODBUS DEBUG USB SERIAL HW - Port="+Parameters["SerialPort"]+", BaudRate="+Parameters["Mode2"]+", StopBits="+str(StopBits)+", ByteSize="+str(ByteSize)+" Parity="+Parity)
          Domoticz.Debug("MODBUS DEBUG USB SERIAL CMD - Method="+Parameters["Mode1"]+", Address="+UnitAddress+", Register="+Parameters["Password"]+", Function="+Parameters["Username"]+", Data type="+Parameters["Mode6"])
          try:
            client = ModbusSerialClient(method=Parameters["Mode1"], port=Parameters["SerialPort"], stopbits=StopBits, bytesize=ByteSize, parity=Parity, baudrate=int(Parameters["Mode2"]), timeout=1, retries=2)
          except:
            Domoticz.Log("Error opening Serial interface on "+Parameters["SerialPort"])
            Devices[1].Update(0, "0") # Update device in Domoticz

        ###################################
        # pymodbus: RTU over TCP
        ###################################
        if (Parameters["Mode1"] == "rtutcp"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"]+", Address="+UnitAddress+", Port="+Parameters["Port"]+", Register="+Parameters["Password"]+", Data type="+Parameters["Mode6"])
          try:
            client = ModbusTcpClient(host=UnitAddress, port=int(Parameters["Port"]), framer=ModbusRtuFramer, auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening TCP interface on address: "+UnitAddress)
            Devices[1].Update(0, "0") # Update device in Domoticz

        ###################################
        # pymodbusTCP: TCP/IP
        ###################################
        if (Parameters["Mode1"] == "tcpip"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"]+", Address="+UnitAddress+", Port="+Parameters["Port"]+", Unit ID="+UnitIdForIp+", Register="+Parameters["Password"]+", Data type="+Parameters["Mode6"])
          try:
            client = ModbusClient(host=UnitAddress, port=int(Parameters["Port"]), unit_id=UnitIdForIp, auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening TCP/IP interface on address: "+UnitAddress)
            Devices[1].Update(0, "0") # Update device in Domoticz

        ###################################
        # pymodbus section
        ###################################
        if (Parameters["Mode1"] == "rtu" or Parameters["Mode1"] == "ascii" or Parameters["Mode1"] == "rtutcp"):
          try:
            # Which function to execute? RTU/ASCII/RTU over TCP
            if (Parameters["Username"] == "1"): data = client.read_coils(int(Parameters["Password"]), registercount, unit=int(UnitIdForIp))
            if (Parameters["Username"] == "2"): data = client.read_discrete_inputs(int(Parameters["Password"]), registercount, unit=int(UnitIdForIp))
            if (Parameters["Username"] == "3"): data = client.read_holding_registers(int(Parameters["Password"]), registercount, unit=int(UnitIdForIp))
            if (Parameters["Username"] == "4"): data = client.read_input_registers(int(Parameters["Password"]), registercount, unit=int(UnitIdForIp))
            Domoticz.Debug("MODBUS DEBUG RESPONSE: " + str(data))
          except:
            Domoticz.Log("Modbus error communicating! (RTU/ASCII/RTU over TCP), check your settings!")
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz

          try:
            # How to decode the input?
            # Added option to swap bytes (little endian)
            if (Parameters["Mode6"] == "int16s" or Parameters["Mode6"] == "uint16s"): 
              decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Little, wordorder=Endian.Big)
            # Added option to swap words (little endian)
            elif (Parameters["Mode6"] == "int32s" or Parameters["Mode6"] == "uint32s" or Parameters["Mode6"] == "int64s" or Parameters["Mode6"] == "uint64s" 
                  or Parameters["Mode6"] == "float32s" or Parameters["Mode6"] == "float64s"):
              decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big, wordorder=Endian.Little)
            # Otherwise always big endian
            else:
              decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big, wordorder=Endian.Big)

            if (Parameters["Mode6"] == "noco"): value = data
            if (Parameters["Mode6"] == "int8LSB"):
              ignored = decoder.skip_bytes(1)
              value = decoder.decode_8bit_int()
            if (Parameters["Mode6"] == "int8MSB"): value = decoder.decode_8bit_int()
            if (Parameters["Mode6"] == "int16"): value = decoder.decode_16bit_int()
            if (Parameters["Mode6"] == "int16s"): value = decoder.decode_16bit_int()
            if (Parameters["Mode6"] == "int32"): value = decoder.decode_32bit_int()
            if (Parameters["Mode6"] == "int32s"): value = decoder.decode_32bit_int()
            if (Parameters["Mode6"] == "int64"): value = decoder.decode_64bit_int()
            if (Parameters["Mode6"] == "int64s"): value = decoder.decode_64bit_int()
            if (Parameters["Mode6"] == "uint8LSB"):
              ignored = decoder.skip_bytes(1)
              value = decoder.decode_8bit_uint()
            if (Parameters["Mode6"] == "uint8MSB"): value = decoder.decode_8bit_uint()
            if (Parameters["Mode6"] == "uint16"): value = decoder.decode_16bit_uint()
            if (Parameters["Mode6"] == "uint16s"): value = decoder.decode_16bit_uint()
            if (Parameters["Mode6"] == "uint32"): value = decoder.decode_32bit_uint()
            if (Parameters["Mode6"] == "uint32s"): value = decoder.decode_32bit_uint()
            if (Parameters["Mode6"] == "uint64"): value = decoder.decode_64bit_uint()
            if (Parameters["Mode6"] == "uint64s"): value = decoder.decode_64bit_uint()
            if (Parameters["Mode6"] == "float32"): value = decoder.decode_32bit_float()
            if (Parameters["Mode6"] == "float32s"): value = decoder.decode_32bit_float()
            if (Parameters["Mode6"] == "float64"): value = decoder.decode_64bit_float()
            if (Parameters["Mode6"] == "float64s"): value = decoder.decode_64bit_float()
            if (Parameters["Mode6"] == "string2"): value = decoder.decode_string(2)
            if (Parameters["Mode6"] == "string4"): value = decoder.decode_string(4)
            if (Parameters["Mode6"] == "string6"): value = decoder.decode_string(6)
            if (Parameters["Mode6"] == "string8"): value = decoder.decode_string(8)
            Domoticz.Debug("MODBUS DEBUG VALUE: " + str(value))

            # Divide the value (decimal)?
            if (Parameters["Mode5"] == "div0"): value = str(value)
            if (Parameters["Mode5"] == "div10"): value = str(round(value / 10, 1))
            if (Parameters["Mode5"] == "div100"): value = str(round(value / 100, 2))
            if (Parameters["Mode5"] == "div1000"): value = str(round(value / 1000, 3))
            if (Parameters["Mode5"] == "div10000"): value = str(round(value / 10000, 4))
            
            Devices[1].Update(0, value) # Update value in Domoticz

          except:
            Domoticz.Log("Modbus error decoding or received no data (RTU/ASCII/RTU over TCP)!, check your settings!")
            Devices[1].Update(0, "0") # Update value in Domoticz

        ###################################
        # pymodbusTCP section
        ###################################
        if (Parameters["Mode1"] == "tcpip"):
          try:
            # Which function to execute? TCP/IP
            if (Parameters["Username"] == "1"): data = client.read_coils(int(Parameters["Password"]), registercount)
            if (Parameters["Username"] == "2"): data = client.read_discrete_inputs(int(Parameters["Password"]), registercount)
            if (Parameters["Username"] == "3"): data = client.read_holding_registers(int(Parameters["Password"]), registercount)
            if (Parameters["Username"] == "4"): data = client.read_input_registers(int(Parameters["Password"]), registercount)
            Domoticz.Debug("MODBUS DEBUG RESPONSE: " + str(data))
          except:
            Domoticz.Log("Modbus error communicating! (TCP/IP), check your settings!")
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz

          try:
            # How to decode the input?
            # Added option to swap bytes (little endian)
            if (Parameters["Mode6"] == "int16s" or Parameters["Mode6"] == "uint16s"):
              decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Little, wordorder=Endian.Big)
            # Added option to swap words (little endian)
            elif (Parameters["Mode6"] == "int32s" or Parameters["Mode6"] == "uint32s" or Parameters["Mode6"] == "int64s" or Parameters["Mode6"] == "uint64s" 
                  or Parameters["Mode6"] == "float32s" or Parameters["Mode6"] == "float64s"):
              decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big, wordorder=Endian.Little)
            # Otherwise always big endian
            else:
              decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big, wordorder=Endian.Big)

            if (Parameters["Mode6"] == "noco"): value = data
            if (Parameters["Mode6"] == "int8LSB"):
              ignored = decoder.skip_bytes(1)
              value = decoder.decode_8bit_int()
            if (Parameters["Mode6"] == "int8MSB"): value = decoder.decode_8bit_int()
            if (Parameters["Mode6"] == "int16"): value = decoder.decode_16bit_int()
            if (Parameters["Mode6"] == "int16s"): value = decoder.decode_16bit_int()
            if (Parameters["Mode6"] == "int32"): value = decoder.decode_32bit_int()
            if (Parameters["Mode6"] == "int32s"): value = decoder.decode_32bit_int()
            if (Parameters["Mode6"] == "int64"): value = decoder.decode_64bit_int()
            if (Parameters["Mode6"] == "int64s"): value = decoder.decode_64bit_int()
            if (Parameters["Mode6"] == "uint8LSB"):
              ignored = decoder.skip_bytes(1)
              value = decoder.decode_8bit_uint()
            if (Parameters["Mode6"] == "uint8MSB"): value = decoder.decode_8bit_uint()   
            if (Parameters["Mode6"] == "uint16"): value = decoder.decode_16bit_uint()
            if (Parameters["Mode6"] == "uint16s"): value = decoder.decode_16bit_uint()
            if (Parameters["Mode6"] == "uint32"): value = decoder.decode_32bit_uint()
            if (Parameters["Mode6"] == "uint32s"): value = decoder.decode_32bit_uint()
            if (Parameters["Mode6"] == "uint64"): value = decoder.decode_64bit_uint()
            if (Parameters["Mode6"] == "uint64s"): value = decoder.decode_64bit_uint()
            if (Parameters["Mode6"] == "float32"): value = decoder.decode_32bit_float()
            if (Parameters["Mode6"] == "float32s"): value = decoder.decode_32bit_float()
            if (Parameters["Mode6"] == "float64"): value = decoder.decode_64bit_float()
            if (Parameters["Mode6"] == "float64s"): value = decoder.decode_64bit_float()
            if (Parameters["Mode6"] == "string2"): value = decoder.decode_string(2)
            if (Parameters["Mode6"] == "string4"): value = decoder.decode_string(4)
            if (Parameters["Mode6"] == "string6"): value = decoder.decode_string(6)
            if (Parameters["Mode6"] == "string8"): value = decoder.decode_string(8)
            Domoticz.Debug("MODBUS DEBUG VALUE: " + str(value))

            # Divide the value (decimal)?
            if (Parameters["Mode5"] == "div0"): value = str(value)
            if (Parameters["Mode5"] == "div10"): value = str(round(value / 10, 1))
            if (Parameters["Mode5"] == "div100"): value = str(round(value / 100, 2))
            if (Parameters["Mode5"] == "div1000"): value = str(round(value / 1000, 3))
            if (Parameters["Mode5"] == "div10000"): value = str(round(value / 10000, 4))

            if (value != "0"): Devices[1].Update(1, value) # Update value in Domoticz
            
          except:
            Domoticz.Log("Modbus error decoding or received no data (TCP/IP)!, check your settings!")
            Devices[1].Update(0, "0") # Update value in Domoticz

    def UpdateDevice(Unit, nValue, sValue):
        # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
        if (Unit in Devices):
          if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
        return

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
