# Modbus RTU/ASCII/TCP - Universal WRITE Plugin for Domoticz
#
# Author: Sebastiaan Ebeltjes / domoticx.nl
# Serial HW: USB RS485-Serial Stick, like: http://domoticx.nl/webwinkel/index.php?route=product/product&product_id=386
#
# Dependancies:
# - pymodbus AND pymodbusTCP:
#   - Install for python 3.x with: sudo pip3 install -U pymodbus pymodbusTCP
#
# NOTE: Some "name" fields are abused to put in more options ;-)
#
"""
<plugin key="ModbusDEV-WRITE" name="Modbus RTU/ASCII/TCP - WRITE v1.0.7" author="S. Ebeltjes / domoticx.nl" version="1.0.7" externallink="" wikilink="https://github.com/DomoticX/domoticz-modbus/">
    <params>
        <param field="Mode4" label="Debug" width="120px">
            <options>
                <option label="True" value="debug"/>
                <option label="False" value="normal"  default="true" />
            </options>
        </param>
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
        <param field="Address" label="Device address" width="120px" required="true"/>
        <param field="Port" label="Port (TCP)" value="502" width="75px"/>
        <param field="Username" label="Modbus Function" width="280px" required="true">
            <options>
                <option label="Write Single Coil (Function 5)" value="5"/>
                <option label="Write Single Holding Register (Function 6)" value="6" default="true"/>
                <option label="Write Multiple Coils (Function 15)" value="15"/>
                <option label="Write Registers (Function 16)" value="16"/>
            </options>
        </param>
        <param field="Password" label="Register number" width="75px" required="true"/>
        <param field="Mode5" label="Payload ON" width="75px"/>
        <param field="Mode6" label="Payload OFF" width="75px"/>
    </params>
</plugin>
"""
import Domoticz

import sys
sys.path.append('/usr/local/lib/python3.4/dist-packages')
sys.path.append('/usr/local/lib/python3.5/dist-packages')

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient
from pyModbusTCP.client import ModbusClient

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

result=""

class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        # Domoticz.Log("onStart called")
        if Parameters["Mode4"] == "debug": Domoticz.Debugging(1)
        if (len(Devices) == 0): Domoticz.Device(Name="ModbusDEV-WRITE", Unit=1, TypeName="Switch", Image=0, Used=1).Create() # Used=1 to add a switch immediatly!
        DumpConfigToLog()
        Domoticz.Log("Modbus RS485 RTU/ASCII/TCP - Universal WRITE loaded.")

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")
        return

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

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

        # Which payload to execute?
        if (str(Command) == "On"): payload = Parameters["Mode5"]
        if (str(Command) == "Off"): payload = Parameters["Mode6"]

        ###################################
        # pymodbus: RTU / ASCII
        ###################################
        if (Parameters["Mode1"] == "rtu" or Parameters["Mode1"] == "ascii"):
          Domoticz.Debug("MODBUS DEBUG USB SERIAL HW - Port="+Parameters["SerialPort"]+" BaudRate="+Parameters["Mode2"]+" StopBits="+str(StopBits)+" ByteSize="+str(ByteSize)+" Parity="+Parity)
          Domoticz.Debug("MODBUS DEBUG USB SERIAL CMD - Method="+Parameters["Mode1"]+" Address="+Parameters["Address"]+" Register="+Parameters["Password"]+" Function="+Parameters["Username"]+" PayLoadON="+Parameters["Mode5"]+" PayLoadOFF="+Parameters["Mode6"])
          try:
            client = ModbusSerialClient(method=Parameters["Mode1"], port=Parameters["SerialPort"], stopbits=StopBits, bytesize=ByteSize, parity=Parity, baudrate=int(Parameters["Mode2"]), timeout=1, retries=2)
          except:
            Domoticz.Log("Error opening Serial interface on "+Parameters["SerialPort"])
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz

        ###################################
        # pymodbus: RTU over TCP
        ###################################
        if (Parameters["Mode1"] == "rtutcp"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"]+" Address="+Parameters["Address"]+" Port="+Parameters["Port"]+" PayLoadON="+Parameters["Mode5"]+" PayLoadOFF="+Parameters["Mode6"])
          try:
            client = ModbusTcpClient(host=Parameters["Address"], port=int(Parameters["Port"]), timeout=5)
          except:
            Domoticz.Log("Error opening TCP interface on adress: "+Parameters["Address"])
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz

        ###################################
        # pymodbusTCP: TCP/IP
        ###################################
        if (Parameters["Mode1"] == "tcpip"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"]+", Address="+Parameters["Address"]+", Port="+Parameters["Port"]+", Register="+Parameters["Password"]+", Data type="+Parameters["Mode6"])
          try:
            client = ModbusClient(host=Parameters["Address"], port=int(Parameters["Port"]), auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening TCP/IP interface on address: "+Parameters["Address"])
            Devices[1].Update(0, "0") # Update device in Domoticz

        ###################################
        # pymodbus section
        ###################################
        if (Parameters["Mode1"] == "rtu" or Parameters["Mode1"] == "ascii" or Parameters["Mode1"] == "rtutcp"):
          try:
            # Which function to execute? RTU/ASCII/RTU over TCP
            if (Parameters["Username"] == "5"): result = client.write_coil(int(Parameters["Password"]), int(payload, 16), unit=int(Parameters["Address"]))
            if (Parameters["Username"] == "6"): result = client.write_register(int(Parameters["Password"]), int(payload, 16), unit=int(Parameters["Address"]))
            if (Parameters["Username"] == "15"): result = client.write_coils(int(Parameters["Password"]), int(payload, 16), unit=int(Parameters["Address"]))
            if (Parameters["Username"] == "16"): result = client.write_registers(int(Parameters["Password"]), int(payload, 16), unit=int(Parameters["Address"]))
            client.close()

            if (str(Command) == "On"): Devices[1].Update(1, "1") # Update device to ON in Domoticz
            if (str(Command) == "Off"): Devices[1].Update(0, "0") # Update device to OFF in Domoticz
          except:
            Domoticz.Log("Modbus error communicating! (RTU/ASCII/RTU over TCP), check your settings!")
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz

        ###################################
        # pymodbusTCP section
        ###################################
        if (Parameters["Mode1"] == "tcpip"):
          try:
            # Which function to execute? TCP/IP
            if (Parameters["Username"] == "5"): data = client.write_single_coil(int(Parameters["Password"]), int(payload))
            if (Parameters["Username"] == "6"): data = client.write_single_register(int(Parameters["Password"]), int(payload))
            if (Parameters["Username"] == "15"): data = client.write_multiple_coils(int(Parameters["Password"]), [payload])  # TODO split up multiple bytes to proper array.
            if (Parameters["Username"] == "16"): data = client.write_multiple_registers(int(Parameters["Password"]), [payload]) # TODO split up multiple bytes to proper array.
            client.close()

            if (str(Command) == "On"): Devices[1].Update(1, "1") # Update device to ON in Domoticz
            if (str(Command) == "Off"): Devices[1].Update(0, "0") # Update device to OFF in Domoticz
          except:
            Domoticz.Log("Modbus error communicating! (TCP/IP), check your settings!")
            Devices[1].Update(0, "0") # Update device to OFF in Domoticz

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        # Domoticz.Log("onHeartbeat called")
        return

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