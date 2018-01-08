# ModbusRTU - SWITCH (USB RS485-Serial) Plugin for Domoticz
#
# Author: Sebastiaan Ebeltjes / domoticx.nl
#
# Install modbus library: 
#
"""
<plugin key="ModbusRTU" name="ModbusRTU - Universal WRITE (USB RS485-Serial)" author="S. Ebeltjes / domoticx.nl" version="1.0.0" externallink="" wikilink="">
    <params>
        <param field="SerialPort" label="Serial Port" width="150px" required="true"/>
        <param field="Mode1" label="BaudRate" width="60px" required="true">
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
        <param field="Mode2" label="StopBits" width="60px" required="true">
            <options>
                <option label="1" value="1" default="true"/>
                <option label="2" value="2"/>
            </options>
        </param>
        <param field="Mode3" label="ByteSize" width="60px" required="true">
            <options>
                <option label="7" value="7"/>
                <option label="8" value="8" default="true"/>
            </options>
        </param>
        <param field="Mode4" label="Parity" width="60px" required="true">
            <options>
                <option label="None" value="N" default="true"/>
                <option label="Even" value="E"/>
                <option label="Odd" value="O"/>
            </options>
        </param>
        <param field="Address" label="Device adress" width="75px" required="true"/>
        <param field="Username" label="Functie" width="280px" required="true">
            <options>
                <option label="Write Single Coil (Function 5)" value="5"/>
                <option label="Write Single Holding Register (Function 6)" value="6" default="true"/>
                <option label="Write Multiple Coils (Function 15)" value="15"/>
                <option label="Write Registers (Function 16)" value="16"/>
            </options>
        </param>
        <param field="Port" label="Register" width="75px" required="true"/>
        <param field="Mode5" label="PayLoad ON (HEX)" width="75px"/>
        <param field="Mode6" label="PayLoad OFF (HEX)" width="75px"/>
    </params>
</plugin>
"""
import Domoticz

import sys
sys.path.append('/usr/local/lib/python3.4/dist-packages/pyserial-3.3-py3.5.egg')
sys.path.append('/usr/local/lib/python3.4/dist-packages')
sys.path.append('/usr/local/lib/python3.5/dist-packages/pyserial-3.3-py3.5.egg')
sys.path.append('/usr/local/lib/python3.5/dist-packages')

from pymodbus3.client.sync import ModbusSerialClient

class BasePlugin:
    enabled = False
    global data
    def __init__(self):
        return

    def onStart(self):
       #Domoticz.Log("onStart called")
       if (len(Devices) == 0): Domoticz.Device(Name="ModbusRTU", Unit=1, TypeName="Switch", Image=0, Used=1).Create() #Used=1 to add a switch immediatly!
       DumpConfigToLog()
       Domoticz.Log("ModbusRTU - Universal WRITE (USB RS485-Serial) loaded.")
       return

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")
        return

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        #Domoticz.Log("onCommand called")
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        Domoticz.Log("MODBUS DEBUG HW - Port="+Parameters["SerialPort"]+" BaudRate="+Parameters["Mode1"]+" StopBits="+Parameters["Mode2"]+" ByteSize="+Parameters["Mode3"]+" Parity="+Parameters["Mode4"]) # DEBUG LINE
        Domoticz.Log("MODBUS DEBUG CMD - Address="+Parameters["Address"]+" Register="+Parameters["Port"]+" Function="+Parameters["Username"]+" PayLoadON="+Parameters["Mode5"]+" PayLoadOFF="+Parameters["Mode6"]) # DEBUG LINE

        #Which payload to execute?
        if (str(Command) == "On"): payload = Parameters["Mode5"]
        if (str(Command) == "Off"): payload = Parameters["Mode6"]

        try:
          client = ModbusSerialClient(method="rtu", port=Parameters["SerialPort"], stopbits=int(Parameters["Mode2"]), bytesize=int(Parameters["Mode3"]), parity=Parameters["Mode4"], baudrate=int(Parameters["Mode1"]), timeout=1, retries=2)

          #Which function to execute?
          if (Parameters["Username"] == "5"): data = client.write_coil(int(Parameters["Port"]), int(payload, 16), unit=int(Parameters["Address"]))
          if (Parameters["Username"] == "6"): data = client.write_register(int(Parameters["Port"]), int(payload, 16), unit=int(Parameters["Address"]))
          if (Parameters["Username"] == "15"): data = client.write_coils(int(Parameters["Port"]), int(payload, 16), unit=int(Parameters["Address"]))
          if (Parameters["Username"] == "16"): data = client.write_registers(int(Parameters["Port"]), int(payload, 16), unit=int(Parameters["Address"]))

	  #Domoticz.Log(data)
          client.close()
          if (str(Command) == "On"): Devices[1].Update(1, "1") #Update device to ON in Domoticz
          if (str(Command) == "Off"): Devices[1].Update(0, "0") #Update device to OFF in Domoticz

        except:
          Domoticz.Log("Error communicating with RS485-Serial interface on "+Parameters["SerialPort"])
          Devices[1].Update(0, "0") #Update device to OFF in Domoticz

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        #Domoticz.Log("onHeartbeat called")
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