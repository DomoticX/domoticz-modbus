# Modbus RS485 RTU/ASCII/TCP - Universal READ Plugin for Domoticz
#
# Author: Sebastiaan Ebeltjes / domoticx.nl
# Serial HW: USB RS485-Serial Stick, like: http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386
#
# Dependancies:
# - PYMODBUS v1.4.0 or higher
#   - Install for python 3.x with: sudo pip3 install -U pymodbus
#
# NOTE: Some "name" fields are abused to put in more options ;-)
#
"""
<plugin key="Modbus" name="Modbus RS485 RTU/ASCII/TCP - READ v1.0.4" author="S. Ebeltjes / domoticx.nl" version="1.0.4" externallink="" wikilink="https://github.com/DomoticX/domoticz-modbus/">
    <params>
        <param field="Mode4" label="Debug" width="120px">
            <options>
                <option label="True" value="debug"/>
                <option label="False" value="normal"  default="true" />
            </options>
        </param>
        <param field="Mode1" label="Method" width="60px" required="true">
            <options>
                <option label="RTU" value="rtu" default="true"/>
                <option label="ASCII" value="ascii"/>
                <option label="TCP" value="tcp"/>
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
        <param field="Address" label="Device address" width="120px" required="true"/>
        <param field="Port" label="Port (TCP)" width="75px"/>
        <param field="Username" label="Function" width="220px" required="true">
            <options>
                <option label="Read Coil (Function 1)" value="1"/>
                <option label="Read Discrete Input (Function 2)" value="2"/>
                <option label="Read Holding Registers (Function 3)" value="3"/>
                <option label="Read Input Registers (Function 4)" value="4" default="true"/>
            </options>
        </param>
        <param field="Password" label="Register start" width="75px" required="true"/>
        <param field="Mode5" label="Registers to read" width="75px"/>
        <param field="Mode6" label="Data type" width="180px" required="true">
            <options>
                <option label="8-Bit INT (1 register long)" value="8int"/>
                <option label="16-Bit INT (1 register long)" value="16int"/>
                <option label="32-Bit INT (2 registers long)" value="32int"/>
                <option label="64-Bit INT (4 registers long)" value="64int"/>
                <option label="8-Bit UINT (1 register long)" value="8uint"/>
                <option label="16-Bit UINT (1 register long)" value="16uint" default="true"/>
                <option label="32-Bit UINT (2 registers long)" value="32uint"/>
                <option label="64-Bit UINT (4 registers long)" value="64uint"/>
                <option label="32-Bit FLOAT (2 registers long)" value="float32"/>
                <option label="64-Bit FLOAT (4 registers long)" value="float64"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

import sys
sys.path.append('/usr/local/lib/python3.4/dist-packages')
sys.path.append('/usr/local/lib/python3.5/dist-packages')

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

result=""
data=[]

class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        #Domoticz.Log("onStart called")
        if Parameters["Mode4"] == "debug": Domoticz.Debugging(1)
        if (len(Devices) == 0): Domoticz.Device(Name="ModbusDEV-READ", Unit=1, TypeName="Custom", Image=0, Used=1).Create() # Used=1 to add a switch immediatly!
        DumpConfigToLog()
        Domoticz.Log("Modbus RS485 RTU/ASCII/TCP - Universal READ loaded.")
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

        if (Parameters["Mode1"] == "rtu" or Parameters["Mode1"] == "ascii"):
          Domoticz.Debug("MODBUS DEBUG USB SERIAL HW - Port="+Parameters["SerialPort"]+" BaudRate="+Parameters["Mode2"]+" StopBits="+str(StopBits)+" ByteSize="+str(ByteSize)+" Parity="+Parity)
          Domoticz.Debug("MODBUS DEBUG USB SERIAL CMD - Method="+Parameters["Mode1"]+" Address="+Parameters["Address"]+" Register="+Parameters["Password"]+" Function="+Parameters["Username"]+" Registers to read="+Parameters["Mode5"]+" Data type="+Parameters["Mode6"])
          try:
            client = ModbusSerialClient(method=Parameters["Mode1"], port=Parameters["SerialPort"], stopbits=StopBits, bytesize=ByteSize, parity=Parity, baudrate=int(Parameters["Mode2"]), timeout=1, retries=2)
          except:
            Domoticz.Log("Error opening RS485-Serial interface on "+Parameters["SerialPort"])
            Devices[1].Update(0, "0") # Update device in Domoticz

        if (Parameters["Mode1"] == "tcp"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"]+" Address="+Parameters["Address"]+" Port="+Parameters["Port"]+" Register="+Parameters["Password"]+" Registers to read="+Parameters["Mode5"]+" Data type="+Parameters["Mode6"])
          try:
            client = ModbusTcpClient(host=Parameters["Address"], port=int(Parameters["Port"]))
          except:
            Domoticz.Log("Error opening TCP interface on address: "+Parameters["Address"])
            Devices[1].Update(0, "0") # Update device in Domoticz

        try:
          # Which function to execute?
          if (Parameters["Username"] == "1"): data = client.read_coils(int(Parameters["Password"]), int(Parameters["Mode5"]), unit=int(Parameters["Address"]))
          if (Parameters["Username"] == "2"): data = client.read_discrete_inputs(int(Parameters["Password"]), int(Parameters["Mode5"]), unit=int(Parameters["Address"]))
          if (Parameters["Username"] == "3"): data = client.read_holding_registers(int(Parameters["Password"]), int(Parameters["Mode5"]), unit=int(Parameters["Address"]))
          if (Parameters["Username"] == "4"): data = client.read_input_registers(int(Parameters["Password"]), int(Parameters["Mode5"]), unit=int(Parameters["Address"]))
          client.close()
        except:
          Domoticz.Log("Modbus error communicating!, check your settings!")
          Devices[1].Update(0, "0") # Update device to OFF in Domoticz

        try:
          # How to decode the input?
          decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
          if (Parameters["Mode6"] == "8int"): value = str(round(decoder.decode_8bit_int(), 2))
          if (Parameters["Mode6"] == "16int"): value = str(round(decoder.decode_16bit_int(), 2))
          if (Parameters["Mode6"] == "32int"): value = str(round(decoder.decode_32bit_int(), 2))
          if (Parameters["Mode6"] == "64int"): value = str(round(decoder.decode_64bit_int(), 2))
          if (Parameters["Mode6"] == "8uint"): value = str(round(decoder.decode_8bit_uint(), 2))
          if (Parameters["Mode6"] == "16uint"): value = str(round(decoder.decode_16bit_uint(), 2))
          if (Parameters["Mode6"] == "32uint"): value = str(round(decoder.decode_32bit_uint(), 2))
          if (Parameters["Mode6"] == "64uint"): value = str(round(decoder.decode_64bit_uint(), 2))
          if (Parameters["Mode6"] == "float32"): value = str(round(decoder.decode_32bit_float(), 2))
          if (Parameters["Mode6"] == "float64"): value = str(round(decoder.decode_64bit_float(), 2))
          Domoticz.Debug("MODBUS DEBUG VALUE: "+value)
          Devices[1].Update(0, value) # Update value in Domoticz
        except:
          Domoticz.Log("Modbus error decoding (or recieved no data)!, check your settings!")
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