# Modbus RTU/ASCII/TCP - Universal READ Plugin for Domoticz
#
# Tested on domoticz 2020.2 with Python v3.7.3 and pymodbus v2.3.0
#
# Author: Sebastiaan Ebeltjes / DomoticX.nl
# RTU Serial HW: USB RS485-Serial Stick, like https://webshop.domoticx.nl/index.php?route=product/search&search=RS485%20RTU%20USB
#
# Dependancies:
# - pymodbus AND pymodbusTCP:
#   - Install for python3 with: sudo pip3 install -U pymodbus pymodbusTCP
#

"""
<plugin key="Modbus" name="Modbus RTU/ASCII/TCP - READ v2020.2B" author="S. Ebeltjes / domoticx.nl" version="2020.2B" externallink="" wikilink="https://github.com/DomoticX/domoticz-modbus">
    <params>
        <param field="Mode1" label="Communication Mode" width="160px" required="true">
            <options>
                <option label="RTU" value="rtu:rtu" default="true"/>
				<option label="RTU (+DEBUG)" value="rtu:debug"/>
                <option label="ASCII" value="ascii:ascii"/>
				<option label="ASCII (+DEBUG)" value="ascii:debug"/>
                <option label="RTU over TCP" value="rtutcp:rtutcp"/>
				<option label="RTU over TCP (+DEBUG)" value="rtutcp:debug"/>
                <option label="TCP/IP" value="tcpip:tcpip"/>
                <option label="TCP/IP (+DEBUG)" value="tcpip:debug"/>
            </options>
        </param>
        <param field="SerialPort" label="RTU - Serial Port" width="120px"/>
        <param field="Mode3" label="RTU - Port settings" width="260px">
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
        <param field="Mode2" label="RTU - Baudrate" width="70px">
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
        <param field="Address" label="TCP - IP:Port" width="140px" default="192.168.2.1:501"/>
        <param field="Password" label="Device ID:Pollingrate(sec)" width="50px" default="1:10" required="true"/>
        <param field="Username" label="Modbus Function" width="250px" required="true">
            <options>
                <option label="Read Coil (Function 1)" value="1"/>
                <option label="Read Discrete Input (Function 2)" value="2"/>
                <option label="Read Holding Registers (Function 3)" value="3"/>
                <option label="Read Input Registers (Function 4)" value="4" default="true"/>
            </options>
        </param>
        <param field="Port" label="Register number" width="50px" default="1" required="true"/>
        <param field="Mode6" label="Data type" width="180px" required="true">
            <options>
                <option label="No conversion (1 register)" value="noco"/>
                <option label="BOOL (TRUE/FALSE)" value="bool"/>
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
        <param field="Mode4" label="Sensor type" width="160px" required="true" value="Custom">
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
import pymodbus

from pymodbus.client.sync import ModbusSerialClient # RTU
from pymodbus.client.sync import ModbusTcpClient    # RTU over TCP
from pymodbus.transaction import ModbusRtuFramer    # RTU over TCP
from pyModbusTCP.client import ModbusClient         # TCP/IP
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
        
	    # Set debug yes/no
        Domoticz_Setting_Debug = Parameters["Mode1"].split(":")
        if (Domoticz_Setting_Debug[1] == "debug"):
          Domoticz.Debugging(1) #Enable debugging
          Domoticz.Log("***** NOTIFICATION: Debug enabled!")

        # Set device pollrate (heartbeat)
        Domoticz_Setting_Device_IDPOL = Parameters["Password"].split(":") # Split ID an pollrate setting ID:POLL (Heartbeat)
        Domoticz_Setting_Device_Pollrate = 10 # Default
        if len(Domoticz_Setting_Device_IDPOL) > 1: Domoticz_Setting_Device_Pollrate = Domoticz_Setting_Device_IDPOL[1]

        Domoticz.Heartbeat(int(Domoticz_Setting_Device_Pollrate))
        Domoticz.Log("***** NOTIFICATION: Pollrate (heartbeat): "+Domoticz_Setting_Device_Pollrate+" seconds.")

        # Dependancies notification
        if (float(Parameters["DomoticzVersion"]) < float("2020.2")): Domoticz.Log("[b]***** NOTIFICATION: Domoticz version is outdated/not supported, please update![/b]")	
        if (float(sys.version[:1]) < 3): Domoticz.Log("***** NOTIFICATION: Python3 should be used!")	
        if (float(pymodbus.__version__[:3]) < float("2.3")): Domoticz.Log("***** NOTIFICATION: Pymodbus version is outdated, please update!")	
		
        #Due to the lack of more parameter posibility, the name will be the hardware name
        Domoticz_Setting_Sensor_Type = Parameters["Mode4"]
		
        if (len(Devices) == 0): Domoticz.Device(Name=" ",  Unit=1, TypeName=Domoticz_Setting_Sensor_Type, Image=0, Used=1).Create() #Added sensor type
        DumpConfigToLog()
        Domoticz.Log("Modbus RTU/ASCII/TCP - Universal READ loaded!, using python v" + sys.version[:6] + " and pymodbus v" + pymodbus.__version__)
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

        # Convert "option names" to variables for easy reading and debugging.
        # Note:
        # Parameters["Port"] cannot accept other then int! (e.g. 192.192.0.0 will result in 192)

		
        Tempdata = Parameters["Mode1"].split(":")
        Domoticz_Setting_Communication_Mode = Tempdata[0]
        Domoticz_Setting_Serial_Port = Parameters["SerialPort"]
        Domoticz_Setting_Baudrate = Parameters["Mode2"]
        Domoticz_Setting_Port_Mode = Parameters["Mode3"]
        
        Domoticz_Setting_Device_IDPOL = Parameters["Password"].split(":") # Split ID an pollrate setting ID:POLL (Heartbeat)
        Domoticz_Setting_Device_ID = 1 # Default
        if len(Domoticz_Setting_Device_IDPOL) > 0: Domoticz_Setting_Device_ID = Domoticz_Setting_Device_IDPOL[0]
        Domoticz_Setting_Device_Pollrate = 10 # Default
        if len(Domoticz_Setting_Device_IDPOL) > 1: Domoticz_Setting_Device_Pollrate = Domoticz_Setting_Device_IDPOL[1]

        Domoticz_Setting_TCP_IPPORT = Parameters["Address"].split(":") # Split address and port setting TCP:IP
        Domoticz_Setting_TCP_IP = 0 # Default
        if len(Domoticz_Setting_TCP_IPPORT) > 0: Domoticz_Setting_TCP_IP = Domoticz_Setting_TCP_IPPORT[0]
        Domoticz_Setting_TCP_PORT = 0 # Default
        if len(Domoticz_Setting_TCP_IPPORT) > 1: Domoticz_Setting_TCP_PORT = Domoticz_Setting_TCP_IPPORT[1]
		 
        Domoticz_Setting_Modbus_Function = Parameters["Username"]
        Domoticz_Setting_Register_Number = Parameters["Port"]
        Domoticz_Setting_Data_Type = Parameters["Mode6"]
        Domoticz_Setting_Divide_Value = Parameters["Mode5"]
        Domoticz_Setting_Sensor_Type = Parameters["Mode4"]
		
        # RTU - Serial port settings
        if (Domoticz_Setting_Port_Mode == "S1B7PN"): StopBits, ByteSize, Parity = 1, 7, "N"
        if (Domoticz_Setting_Port_Mode == "S1B7PE"): StopBits, ByteSize, Parity = 1, 7, "E"
        if (Domoticz_Setting_Port_Mode == "S1B7PO"): StopBits, ByteSize, Parity = 1, 7, "O"
        if (Domoticz_Setting_Port_Mode == "S1B8PN"): StopBits, ByteSize, Parity = 1, 8, "N"
        if (Domoticz_Setting_Port_Mode == "S1B8PE"): StopBits, ByteSize, Parity = 1, 8, "E"
        if (Domoticz_Setting_Port_Mode == "S1B8PO"): StopBits, ByteSize, Parity = 1, 8, "O"
        if (Domoticz_Setting_Port_Mode == "S2B7PN"): StopBits, ByteSize, Parity = 2, 7, "N"
        if (Domoticz_Setting_Port_Mode == "S2B7PE"): StopBits, ByteSize, Parity = 2, 7, "E"
        if (Domoticz_Setting_Port_Mode == "S2B7PO"): StopBits, ByteSize, Parity = 2, 7, "O"
        if (Domoticz_Setting_Port_Mode == "S2B8PN"): StopBits, ByteSize, Parity = 2, 8, "N"
        if (Domoticz_Setting_Port_Mode == "S2B8PE"): StopBits, ByteSize, Parity = 2, 8, "E"
        if (Domoticz_Setting_Port_Mode == "S2B8PO"): StopBits, ByteSize, Parity = 2, 8, "O"

        # Read n registers depending on data type
	    # Added additional options for byte/word swapping
        registercount = 1 # Default
        if (Domoticz_Setting_Data_Type == "noco"): registercount = 1
        if (Domoticz_Setting_Data_Type == "bool"): registercount = 1
        if (Domoticz_Setting_Data_Type == "int8LSB"): registercount = 1
        if (Domoticz_Setting_Data_Type == "int8MSB"): registercount = 1
        if (Domoticz_Setting_Data_Type == "int16"): registercount = 1
        if (Domoticz_Setting_Data_Type == "int16s"): registercount = 1
        if (Domoticz_Setting_Data_Type == "int32"): registercount = 2
        if (Domoticz_Setting_Data_Type == "int32s"): registercount = 2
        if (Domoticz_Setting_Data_Type == "int64"): registercount = 4
        if (Domoticz_Setting_Data_Type == "int64s"): registercount = 4
        if (Domoticz_Setting_Data_Type == "uint8LSB"): registercount = 1
        if (Domoticz_Setting_Data_Type == "uint8MSB"): registercount = 1
        if (Domoticz_Setting_Data_Type == "uint16"): registercount = 1
        if (Domoticz_Setting_Data_Type == "uint16s"): registercount = 1
        if (Domoticz_Setting_Data_Type == "uint32"): registercount = 2
        if (Domoticz_Setting_Data_Type == "uint32s"): registercount = 2
        if (Domoticz_Setting_Data_Type == "uint64"): registercount = 4
        if (Domoticz_Setting_Data_Type == "uint64s"): registercount = 4
        if (Domoticz_Setting_Data_Type == "float32"): registercount = 2
        if (Domoticz_Setting_Data_Type == "float32s"): registercount = 2
        if (Domoticz_Setting_Data_Type == "float64"): registercount = 4
        if (Domoticz_Setting_Data_Type == "float64s"): registercount = 4
        if (Domoticz_Setting_Data_Type == "string2"): registercount = 2
        if (Domoticz_Setting_Data_Type == "string4"): registercount = 4
        if (Domoticz_Setting_Data_Type == "string6"): registercount = 6
        if (Domoticz_Setting_Data_Type == "string8"): registercount = 8

        ########################################
        # SET HARDWARE - pymodbus: RTU / ASCII
        ########################################
        if (Domoticz_Setting_Communication_Mode == "rtu" or Domoticz_Setting_Communication_Mode == "ascii"):
          Domoticz.Debug("MODBUS DEBUG - PORT: Port="+Domoticz_Setting_Serial_Port+", BaudRate="+Domoticz_Setting_Baudrate+", StopBits="+str(StopBits)+", ByteSize="+str(ByteSize)+" Parity="+Parity)
          Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+Domoticz_Setting_Communication_Mode+", Device ID="+Domoticz_Setting_Device_ID+", Register="+Domoticz_Setting_Register_Number+", Function="+Domoticz_Setting_Modbus_Function+", Data type="+Domoticz_Setting_Data_Type+", Pollrate(sec)="+Domoticz_Setting_Device_Pollrate)
          try:
            client = ModbusSerialClient(method=Domoticz_Setting_Communication_Mode, port=Domoticz_Setting_Serial_Port, stopbits=StopBits, bytesize=ByteSize, parity=Parity, baudrate=int(Domoticz_Setting_Baudrate), timeout=1, retries=2)
          except:
            Domoticz.Log("Error opening Serial interface on "+Domoticz_Setting_Serial_Port)
            Devices[1].Update(0, "0") # Update device in Domoticz

        ########################################
        # SET HARDWARE - pymodbus: RTU over TCP
        ########################################
        if (Domoticz_Setting_Communication_Mode == "rtutcp"):
          Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+Domoticz_Setting_Communication_Mode+", Device ID="+Domoticz_Setting_Device_ID+", Port="+Domoticz_Setting_TCP_PORT+", Register="+Domoticz_Setting_Register_Number+", Data type="+Domoticz_Setting_Data_Type+", Pollrate(sec)="+Domoticz_Setting_Device_Pollrate)
          try:
            client = ModbusTcpClient(host=Domoticz_Setting_TCP_IP, port=int(Domoticz_Setting_TCP_PORT), framer=ModbusRtuFramer, auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening RTU over TCP interface on address: "+Domoticz_Setting_TCP_IPPORT)
            Devices[1].Update(0, "0") # Update device in Domoticz

        ########################################
        # SET HARDWARE - pymodbusTCP: TCP/IP
        ########################################
        if (Domoticz_Setting_Communication_Mode == "tcpip"):
          Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+Domoticz_Setting_Communication_Mode+", Device ID="+Domoticz_Setting_Device_ID+", Port="+Domoticz_Setting_TCP_PORT+", Unit ID="+Domoticz_Setting_Device_ID+", Register="+Domoticz_Setting_Register_Number+", Data type="+Domoticz_Setting_Data_Type+", Pollrate(sec)="+Domoticz_Setting_Device_Pollrate)
          try:
            client = ModbusClient(host=Domoticz_Setting_TCP_IP, port=int(Domoticz_Setting_TCP_PORT), unit_id=Domoticz_Setting_Device_ID, auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening TCP/IP interface on address: "+Domoticz_Setting_TCP_IPPORT)
            Devices[1].Update(0, "0") # Update device in Domoticz

        ########################################
        # GET DATA - pymodbus: RTU / ASCII / RTU over TCP
        ########################################
        if (Domoticz_Setting_Communication_Mode == "rtu" or Domoticz_Setting_Communication_Mode == "ascii" or Domoticz_Setting_Communication_Mode == "rtutcp"):
          try:
            # Which function to execute? RTU/ASCII/RTU over TCP
            if (Domoticz_Setting_Modbus_Function == "1"): data = client.read_coils(int(Domoticz_Setting_Register_Number), registercount, unit=int(Domoticz_Setting_Device_ID))
            if (Domoticz_Setting_Modbus_Function == "2"): data = client.read_discrete_inputs(int(Domoticz_Setting_Register_Number), registercount, unit=int(Domoticz_Setting_Device_ID))
            if (Domoticz_Setting_Modbus_Function == "3"): data = client.read_holding_registers(int(Domoticz_Setting_Register_Number), registercount, unit=int(Domoticz_Setting_Device_ID))
            if (Domoticz_Setting_Modbus_Function == "4"): data = client.read_input_registers(int(Domoticz_Setting_Register_Number), registercount, unit=int(Domoticz_Setting_Device_ID))
            Domoticz.Debug("MODBUS DEBUG - RESPONSE: " + str(data))
          except:
            Domoticz.Log("Modbus error communicating! (RTU/ASCII/RTU over TCP), check your settings!")
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz


        ########################################
        # GET DATA - pymodbusTCP: TCP/IP
        ########################################
        if (Domoticz_Setting_Communication_Mode == "tcpip"):
          try:
            # Which function to execute? TCP/IP
            if (Domoticz_Setting_Modbus_Function == "1"): data = client.read_coils(int(Domoticz_Setting_Register_Number), registercount)
            if (Domoticz_Setting_Modbus_Function == "2"): data = client.read_discrete_inputs(int(Domoticz_Setting_Register_Number), registercount)
            if (Domoticz_Setting_Modbus_Function == "3"): data = client.read_holding_registers(int(Domoticz_Setting_Register_Number), registercount)
            if (Domoticz_Setting_Modbus_Function == "4"): data = client.read_input_registers(int(Domoticz_Setting_Register_Number), registercount)
            Domoticz.Debug("MODBUS DEBUG RESPONSE: " + str(data))
          except:
            Domoticz.Log("Modbus error communicating! (TCP/IP), check your settings!")
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz


        ########################################
        # DECODE DATA
        ########################################
        try:
          # Added option to swap bytes (little endian)
          if (Domoticz_Setting_Data_Type == "int16s" or Domoticz_Setting_Data_Type == "uint16s"):
            decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Little, wordorder=Endian.Big)
          # Added option to swap words (little endian)
          elif (Domoticz_Setting_Data_Type == "int32s" or Domoticz_Setting_Data_Type == "uint32s" or Domoticz_Setting_Data_Type == "int64s" or Domoticz_Setting_Data_Type == "uint64s" 
                or Domoticz_Setting_Data_Type == "float32s" or Domoticz_Setting_Data_Type == "float64s"):
            decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Little)
          # Otherwise always big endian
          else:
            decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)

          Domoticz.Debug("MODBUS DEBUG - VALUE before conversion: " + str(data.registers[0]))
		 
          if (Domoticz_Setting_Data_Type == "noco"): value = data.registers[0]
          if (Domoticz_Setting_Data_Type == "bool"): value = bool(data.registers[0])
          if (Domoticz_Setting_Data_Type == "int8LSB"):
            ignored = decoder.skip_bytes(1)
            value = decoder.decode_8bit_int()
          if (Domoticz_Setting_Data_Type == "int8MSB"): value = decoder.decode_8bit_int()
          if (Domoticz_Setting_Data_Type == "int16"): value = decoder.decode_16bit_int()
          if (Domoticz_Setting_Data_Type == "int16s"): value = decoder.decode_16bit_int()
          if (Domoticz_Setting_Data_Type == "int32"): value = decoder.decode_32bit_int()
          if (Domoticz_Setting_Data_Type == "int32s"): value = decoder.decode_32bit_int()
          if (Domoticz_Setting_Data_Type == "int64"): value = decoder.decode_64bit_int()
          if (Domoticz_Setting_Data_Type == "int64s"): value = decoder.decode_64bit_int()
          if (Domoticz_Setting_Data_Type == "uint8LSB"):
            ignored = decoder.skip_bytes(1)
            value = decoder.decode_8bit_uint()
          if (Domoticz_Setting_Data_Type == "uint8MSB"): value = decoder.decode_8bit_uint()   
          if (Domoticz_Setting_Data_Type == "uint16"): value = decoder.decode_16bit_uint()
          if (Domoticz_Setting_Data_Type == "uint16s"): value = decoder.decode_16bit_uint()
          if (Domoticz_Setting_Data_Type == "uint32"): value = decoder.decode_32bit_uint()
          if (Domoticz_Setting_Data_Type == "uint32s"): value = decoder.decode_32bit_uint()
          if (Domoticz_Setting_Data_Type == "uint64"): value = decoder.decode_64bit_uint()
          if (Domoticz_Setting_Data_Type == "uint64s"): value = decoder.decode_64bit_uint()
          if (Domoticz_Setting_Data_Type == "float32"): value = decoder.decode_32bit_float()
          if (Domoticz_Setting_Data_Type == "float32s"): value = decoder.decode_32bit_float()
          if (Domoticz_Setting_Data_Type == "float64"): value = decoder.decode_64bit_float()
          if (Domoticz_Setting_Data_Type == "float64s"): value = decoder.decode_64bit_float()
          if (Domoticz_Setting_Data_Type == "string2"): value = decoder.decode_string(2)
          if (Domoticz_Setting_Data_Type == "string4"): value = decoder.decode_string(4)
          if (Domoticz_Setting_Data_Type == "string6"): value = decoder.decode_string(6)
          if (Domoticz_Setting_Data_Type == "string8"): value = decoder.decode_string(8)

          # Divide the value (decimal)?
          if (Domoticz_Setting_Divide_Value == "div0"): value = str(value)
          if (Domoticz_Setting_Divide_Value == "div10"): value = str(round(value / 10, 1))
          if (Domoticz_Setting_Divide_Value == "div100"): value = str(round(value / 100, 2))
          if (Domoticz_Setting_Divide_Value == "div1000"): value = str(round(value / 1000, 3))
          if (Domoticz_Setting_Divide_Value == "div10000"): value = str(round(value / 10000, 4))

          Domoticz.Debug("MODBUS DEBUG - VALUE after conversion: " + str(value))

          #if (value != "0"): Devices[1].Update(int(value), str(value)) # Update device value in Domoticz
          #Devices[1].Update(1, value) # Update device value in Domoticz
          #Devices[1].Update(0, int(value))
          #UpdateDevice(1, 100, str(100), TimedOut=0)
          Devices[1].Update(1, value) # Update value
		  
        except:
          Domoticz.Log("Modbus error decoding or received no data (TCP/IP)!, check your settings!")
          Devices[1].Update(1, 0) # Set value to 0 (error)

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
