# Modbus RTU / ASCII / TCP/IP - Universal READ Plugin for Domoticz
#
# Tested on domoticz 2020.2 (stable) with Python v3.7.3 and pymodbus v2.3.0
#
# Author: Sebastiaan Ebeltjes / DomoticX.nl
# RTU Serial HW: USB RS485-Serial Stick, like https://webshop.domoticx.nl/index.php?route=product/search&search=RS485%20RTU%20USB
#
# Dependancies:
# - pymodbus AND pymodbusTCP:
#   - Install for python3 with: sudo pip3 install -U pymodbus pymodbusTCP
#

"""
<plugin key="ModbusWRITE" name="Modbus RTU / ASCII / TCP/IP - WRITE v2021.7" author="S. Ebeltjes / DomoticX.nl" version="2021.7" externallink="http://domoticx.nl" wikilink="https://github.com/DomoticX/domoticz-modbus">
    <description>
        <h3>Modbus RTU / ASCII / TCP/IP - WRITE</h3>
        With this plugin you can write to RS485 Modbus devices with methods RTU/ASCII/TCP<br/>
        <br/>
        <h4>RTU</h4>
        The serial binary communication protocol. It is the communication standard that<br/>
        became widely used and all series of PLC's and other device producers support it.<br/>
        It goes about the network protocol of the 1Master x nSlave type. The Slave devices can be 254 at the most.<br/>
        <h4>ASCII</h4>
        This protocol is similar to Modbus RTU, but the binary content is transformed to common ASCII characters.<br/>
        It is not used as frequently as Modbus RTU.<br/>
        <h4>RTU over TCP</h4> 
        Means a MODBUS RTU packet wrapped in a TCP packet. The message bytes are modified to add the 6 byte MBAP header and remove the two byte CRC.
        <h4>TCP/IP</h4>
        It is a network protocol - classic Ethernet TCP/IP with the 10/100 Mbit/s speed rate, a standard net HW Ethernet card is sufficient.<br/>
        The communication principle (1Master x nSlave) is the same as for Modbus RTU. used port is most likely: 502<br/>
        <br/>
        <h3>Set-up and Configuration:</h3>
        See wiki link above.<br/> 
    </description>
    <params>
        <param field="Mode1" label="Communication Mode" width="160px" required="true">
            <options>
                <option label="RTU" value="rtu:rtu" default="true"/>
                <option label="RTU (+DEBUG)" value="rtu:debug"/>
                <option label="RTU ASCII" value="ascii:ascii"/>
                <option label="RTU ASCII (+DEBUG)" value="ascii:debug"/>
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
        <param field="Address" label="TCP/IP - IP:Port" width="140px" default="192.168.2.1:502"/>
        <param field="Password" label="Device ID" width="50px" default="1" required="true"/>
        <param field="Username" label="Modbus Function" width="280px" required="true">
             <options>
                <option label="Write Single Coil (Function 5)" value="5"/>
                <option label="Write Single Holding Register (Function 6)" value="6" default="true"/>
                <option label="Write Multiple Coils (Function 15)" value="15"/>
                <option label="Write Registers (Function 16)" value="16"/>
            </options>
        </param>
        <param field="Port" label="Register number" width="50px" default="1" required="true"/>
        <param field="Mode4" label="Payload ON" width="75px"/>
        <param field="Mode5" label="Payload OFF" width="75px"/>
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
result=""

class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        try:
          Domoticz.Log("Modbus RTU/ASCII/TCP - Universal WRITE loaded!, using python v" + sys.version[:6] + " and pymodbus v" + pymodbus.__version__)
        except:
          Domoticz.Log("Modbus RTU/ASCII/TCP - Universal WRITE loaded!")

        # Dependancies notification
        try:
          if (float(Parameters["DomoticzVersion"][:6]) < float("2020.2")): Domoticz.Error("WARNING: Domoticz version is outdated/not supported, please update!")
          if (float(sys.version[:1]) < 3): Domoticz.Error("WARNING: Python3 should be used!")	
          if (float(pymodbus.__version__[:3]) < float("2.3")): Domoticz.Error("WARNING: Pymodbus version is outdated, please update!")	
        except:
          Domoticz.Error("WARNING: Dependancies could not be checked!")

        ########################################
        # READ-IN OPTIONS AND SETTINGS
        ########################################
        # Convert "option names" to variables for easy reading and debugging.
        # Note: Parameters["Port"] cannot accept other value then int! (e.g. 192.168.0.0 will result in 192)

        Domoticz_Setting_Communication_MODE = Parameters["Mode1"].split(":") # Split MODE and DEBUG setting MODE:DEBUG
        self.Domoticz_Setting_Communication_Mode = Domoticz_Setting_Communication_MODE[0]
        self.Domoticz_Setting_Serial_Port = Parameters["SerialPort"]
        self.Domoticz_Setting_Baudrate = Parameters["Mode2"]
        self.Domoticz_Setting_Port_Mode = Parameters["Mode3"]
        self.Domoticz_Setting_Modbus_Function = Parameters["Username"]
        self.Domoticz_Setting_Register_Number = Parameters["Port"]
        self.Domoticz_Setting_Payload_ON = Parameters["Mode4"]
        self.Domoticz_Setting_Payload_OFF = Parameters["Mode5"]
        self.Domoticz_Setting_Device_ID = Parameters["Password"]

        self.Domoticz_Setting_TCP_IPPORT = Parameters["Address"].split(":") # Split address and port setting TCP:IP
        self.Domoticz_Setting_TCP_IP = 0 # Default
        if len(self.Domoticz_Setting_TCP_IPPORT) > 0: self.Domoticz_Setting_TCP_IP = self.Domoticz_Setting_TCP_IPPORT[0]
        self.Domoticz_Setting_TCP_PORT = 0 # Default
        if len(self.Domoticz_Setting_TCP_IPPORT) > 1: self.Domoticz_Setting_TCP_PORT = self.Domoticz_Setting_TCP_IPPORT[1]

        # Set debug yes/no
        if (Domoticz_Setting_Communication_MODE[1] == "debug"):
          Domoticz.Debugging(1) # Enable debugging
          DumpConfigToLog()
          Domoticz.Debug("***** NOTIFICATION: Debug enabled!")
        else:
          Domoticz.Debugging(0) # Disable debugging

        # RTU - Serial port settings
        if (self.Domoticz_Setting_Port_Mode == "S1B7PN"): self.StopBits, self.ByteSize, self.Parity = 1, 7, "N"
        if (self.Domoticz_Setting_Port_Mode == "S1B7PE"): self.StopBits, self.ByteSize, self.Parity = 1, 7, "E"
        if (self.Domoticz_Setting_Port_Mode == "S1B7PO"): self.StopBits, self.ByteSize, self.Parity = 1, 7, "O"
        if (self.Domoticz_Setting_Port_Mode == "S1B8PN"): self.StopBits, self.ByteSize, self.Parity = 1, 8, "N"
        if (self.Domoticz_Setting_Port_Mode == "S1B8PE"): self.StopBits, self.ByteSize, self.Parity = 1, 8, "E"
        if (self.Domoticz_Setting_Port_Mode == "S1B8PO"): self.StopBits, self.ByteSize, self.Parity = 1, 8, "O"
        if (self.Domoticz_Setting_Port_Mode == "S2B7PN"): self.StopBits, self.ByteSize, self.Parity = 2, 7, "N"
        if (self.Domoticz_Setting_Port_Mode == "S2B7PE"): self.StopBits, self.ByteSize, self.Parity = 2, 7, "E"
        if (self.Domoticz_Setting_Port_Mode == "S2B7PO"): self.StopBits, self.ByteSize, self.Parity = 2, 7, "O"
        if (self.Domoticz_Setting_Port_Mode == "S2B8PN"): self.StopBits, self.ByteSize, self.Parity = 2, 8, "N"
        if (self.Domoticz_Setting_Port_Mode == "S2B8PE"): self.StopBits, self.ByteSize, self.Parity = 2, 8, "E"
        if (self.Domoticz_Setting_Port_Mode == "S2B8PO"): self.StopBits, self.ByteSize, self.Parity = 2, 8, "O"

        if (len(Devices) == 0): Domoticz.Device(Name="ModbusWRITE", Unit=1, TypeName="Switch", Image=0, Used=1).Create() # Used=1 to add a switch immediatly!

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")
        return

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        # ON/OFF payload value
        payload = Level # Set payload from slider/scroll
        # Set payload if a button has been pressed
        if (str(Command) == "On"): payload = self.Domoticz_Setting_Payload_ON
        if (str(Command) == "Off"): payload = self.Domoticz_Setting_Payload_OFF

        ########################################
        # SET HARDWARE - pymodbus: RTU / ASCII
        ########################################
        if (self.Domoticz_Setting_Communication_Mode == "rtu" or self.Domoticz_Setting_Communication_Mode == "ascii"):
          Domoticz.Debug("MODBUS DEBUG - INTERFACE: Port="+self.Domoticz_Setting_Serial_Port+", BaudRate="+self.Domoticz_Setting_Baudrate+", StopBits="+str(self.StopBits)+", ByteSize="+str(self.ByteSize)+" Parity="+self.Parity)
          Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+self.Domoticz_Setting_Communication_Mode+", Device ID="+self.Domoticz_Setting_Device_ID+", Register="+self.Domoticz_Setting_Register_Number+", Function="+self.Domoticz_Setting_Modbus_Function+", Payload="+payload)
          try:
            client = ModbusSerialClient(method=self.Domoticz_Setting_Communication_Mode, port=self.Domoticz_Setting_Serial_Port, stopbits=self.StopBits, bytesize=self.ByteSize, parity=self.Parity, baudrate=int(self.Domoticz_Setting_Baudrate), timeout=2, retries=2)
          except:
            Domoticz.Error("Error opening Serial interface on "+self.Domoticz_Setting_Serial_Port)
            Devices[1].Update(1, "0") # Set value to 0 (error)

        ########################################
        # SET HARDWARE - pymodbus: RTU over TCP
        ########################################
        if (self.Domoticz_Setting_Communication_Mode == "rtutcp"):
          Domoticz.Debug("MODBUS DEBUG - INTERFACE: IP="+self.Domoticz_Setting_TCP_IP+", Port="+self.Domoticz_Setting_TCP_PORT)
          Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+self.Domoticz_Setting_Communication_Mode+", Device ID="+self.Domoticz_Setting_Device_ID+", Register="+self.Domoticz_Setting_Register_Number+", Function="+self.Domoticz_Setting_Modbus_Function+", Payload="+payload)
          try:
            client = ModbusTcpClient(host=self.Domoticz_Setting_TCP_IP, port=int(self.Domoticz_Setting_TCP_PORT), framer=ModbusRtuFramer, auto_open=True, auto_close=True, timeout=2)
          except:
            Domoticz.Error("Error opening RTU over TCP interface on address: "+self.Domoticz_Setting_TCP_IPPORT)
            Devices[1].Update(1, "0") # Set value to 0 (error)

        ########################################
        # SET HARDWARE - pymodbusTCP: TCP/IP
        ########################################
        if (self.Domoticz_Setting_Communication_Mode == "tcpip"):
          Domoticz.Debug("MODBUS DEBUG - INTERFACE: IP="+self.Domoticz_Setting_TCP_IP+", Port="+self.Domoticz_Setting_TCP_PORT)
          Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+self.Domoticz_Setting_Communication_Mode+", Device ID="+self.Domoticz_Setting_Device_ID+", Register="+self.Domoticz_Setting_Register_Number+", Function"+self.Domoticz_Setting_Modbus_Function+", Payload="+payload)
          try:
            client = ModbusClient(host=self.Domoticz_Setting_TCP_IP, port=int(self.Domoticz_Setting_TCP_PORT), unit_id=int(self.Domoticz_Setting_Device_ID), auto_open=True, auto_close=True, timeout=2)
          except:
            Domoticz.Error("Error opening TCP/IP interface on address: "+self.Domoticz_Setting_TCP_IPPORT)
            Devices[1].Update(1, "0") # Set value to 0 (error)

        ########################################
        # WRITE PAYLOAD - pymodbus: RTU / ASCII / RTU over TCP
        ########################################
        if (self.Domoticz_Setting_Communication_Mode == "rtu" or self.Domoticz_Setting_Communication_Mode == "ascii" or self.Domoticz_Setting_Communication_Mode == "rtutcp"):
          try:
            # Function to execute
            if (self.Domoticz_Setting_Modbus_Function == "5"): result = client.write_coil(int(self.Domoticz_Setting_Register_Number), int(payload, 16), unit=int(self.Domoticz_Setting_Device_ID))
            if (self.Domoticz_Setting_Modbus_Function == "6"): result = client.write_register(int(self.Domoticz_Setting_Register_Number), int(payload, 16), unit=int(self.Domoticz_Setting_Device_ID))
            if (self.Domoticz_Setting_Modbus_Function == "15"): result = client.write_coils(int(self.Domoticz_Setting_Register_Number), int(payload, 16), unit=int(self.Domoticz_Setting_Device_ID))
            if (self.Domoticz_Setting_Modbus_Function == "16"): result = client.write_registers(int(self.Domoticz_Setting_Register_Number), int(payload, 16), unit=int(self.Domoticz_Setting_Device_ID))
            client.close()

            Domoticz.Debug("MODBUS DEBUG - RESULT: " + str(result))
            if (str(Command) == "On"): Devices[1].Update(1, "1") # Update device to ON
            if (str(Command) == "Off"): Devices[1].Update(0, "0") # Update device to OFF
          except:
            Domoticz.Error("Modbus error communicating! (RTU/ASCII/RTU over TCP), check your settings!")
            Devices[1].Update(1, "0") # Set value to 0 (error)

        ########################################
        # SET PAYLOAD - pymodbusTCP: TCP/IP
        ########################################
        if (self.Domoticz_Setting_Communication_Mode == "tcpip"):
          try:
            # Function to execute
            if (self.Domoticz_Setting_Modbus_Function == "5"): result = client.write_single_coil(int(self.Domoticz_Setting_Register_Number), int(payload))
            if (self.Domoticz_Setting_Modbus_Function == "6"): result = client.write_single_register(int(self.Domoticz_Setting_Register_Number), int(payload))
            if (self.Domoticz_Setting_Modbus_Function == "15"): result = client.write_multiple_coils(int(self.Domoticz_Setting_Register_Number), [payload])     # TODO split up multiple bytes to proper array.
            if (self.Domoticz_Setting_Modbus_Function == "16"): result = client.write_multiple_registers(int(self.Domoticz_Setting_Register_Number), [payload]) # TODO split up multiple bytes to proper array.
            client.close()

            Domoticz.Debug("MODBUS DEBUG - RESULT: " + str(result))
            if (str(Command) == "On"): Devices[1].Update(1, "1") # Update device to ON
            if (str(Command) == "Off"): Devices[1].Update(0, "0") # Update device to OFF
          except:
            Domoticz.Error("Modbus error communicating! (TCP/IP), check your settings!")
            Devices[1].Update(1, "0") # Set value to 0 (error)

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
