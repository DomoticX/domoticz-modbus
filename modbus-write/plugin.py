# Modbus RTU / ASCII / TCP/IP - Universal WRITE Plugin for Domoticz
#
# Original author: Sebastiaan Ebeltjes / DomoticX.nl
# RTU Serial HW: USB RS485-Serial Stick, like https://webshop.domoticx.nl/index.php?route=product/search&search=RS485%20RTU%20USB
#
# Works with both:
# - Domoticz 2024.7 (stable), Python 3.11.2 and pymodbus 3.6.9 (the previous version of this plugin)
# - Domoticz 2026.4, Python 3.13.5 and pymodbus 3.8.6
# The right pymodbus API (framer classes <= 3.7, FramerType enum >= 3.8) is selected automatically.
#
# Changes compared to the 2021.7 version of this plugin:
# - pymodbus 3.8 API support: FramerType, slave= instead of unit=, explicit connect()/close(),
#   no more removed constructor arguments (auto_open/auto_close)
# - TCP/IP mode now uses pymodbus too, so pyModbusTCP is no longer needed
# - the deprecated BinaryPayloadDecoder / Endian imports were removed (they were not used)
# - the response of the device is checked: a failed write is reported instead of switching the device
# - slider/level commands no longer crash, functions 15/16 now send a proper list of values
# - connection errors now say why the connection failed
#
# Dependancies:
# - pymodbus:
#   - Install for python3 with: sudo pip3 install -U pymodbus   (3.6.9 up to 3.8.x are supported)
#     (use a virtual environment or --break-system-packages if your distro blocks pip)
# - pyModbusTCP is NOT needed anymore
#

"""
<plugin key="ModbusWRITE" name="Modbus RTU / ASCII / TCP/IP - WRITE v2026.4" author="S. Ebeltjes / DomoticX.nl" version="2026.4" externallink="http://domoticx.nl" wikilink="https://github.com/DomoticX/domoticz-modbus">
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
        <param field="Port" label="Register number (decimal)" width="50px" default="1" required="true"/>
        <param field="Mode4" label="Payload ON (decimal)" width="75px"/>
        <param field="Mode5" label="Payload OFF (decimal)" width="75px"/>
    </params>
</plugin>
"""

import Domoticz
import os
import sys
import socket
import inspect
import pymodbus

from pymodbus.client import ModbusSerialClient # RTU / ASCII
from pymodbus.client import ModbusTcpClient    # RTU over TCP / TCP/IP

# Framers: pymodbus >= 3.8 uses the FramerType enum, older versions (e.g. 3.6.9) use framer classes.
try:
    from pymodbus import FramerType            # pymodbus >= 3.8
    FRAMERS = {"rtu": FramerType.RTU, "ascii": FramerType.ASCII, "socket": FramerType.SOCKET}
except ImportError:
    try:
        from pymodbus.framer import ModbusRtuFramer, ModbusAsciiFramer, ModbusSocketFramer
    except ImportError:
        from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer, ModbusSocketFramer
    FRAMERS = {"rtu": ModbusRtuFramer, "ascii": ModbusAsciiFramer, "socket": ModbusSocketFramer}

# Number base of the "Payload ON/OFF" fields, per communication mode.
# This is the behaviour of the 2021.7 plugin, kept so existing setups keep writing the same values:
# RTU / ASCII / RTU over TCP read the payload as HEXADECIMAL, TCP/IP reads it as DECIMAL.
# (The labels in the settings screen say "decimal": set the first three to 10 if you want that everywhere.
#  Values 0-9 are identical in both bases.)
PAYLOAD_BASE = {"rtu": 16, "ascii": 16, "rtutcp": 16, "tcpip": 10}


def version_tuple(text):
    """'3.8.6' -> (3, 8, 6); stops at the first non-numeric part (e.g. '3.8.6.dev1')."""
    parts = []
    for part in str(text).split("."):
        digits = ""
        for ch in part:
            if not ch.isdigit():
                break
            digits += ch
        if digits == "":
            break
        parts.append(int(digits))
    return tuple(parts)


def parse_payload(payload, base):
    """The payload is a string from the settings (ON/OFF) or an int (slider level)."""
    if isinstance(payload, str):
        text = payload.strip()
        if text == "":
            raise ValueError("payload is empty, fill in the Payload ON/OFF settings")
        return int(text, base)
    return int(payload)


def unit_kwargs(method, device_id):
    """pymodbus 3.x: unit= was replaced by slave= (named device_id in the newest releases)."""
    try:
        params = inspect.signature(method).parameters
        for name in ("device_id", "slave", "unit"):
            if name in params:
                return {name: device_id}
    except Exception:
        pass
    return {"slave": device_id}


class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        try:
          Domoticz.Log("Modbus RTU/ASCII/TCP - Universal WRITE loaded!, using python v" + sys.version.split()[0] + " and pymodbus v" + pymodbus.__version__)
        except:
          Domoticz.Log("Modbus RTU/ASCII/TCP - Universal WRITE loaded!")

        # Dependancies notification
        try:
          if (version_tuple(Parameters["DomoticzVersion"]) < (2020, 2)): Domoticz.Error("WARNING: Domoticz version is outdated/not supported, please update!")
          if (sys.version_info[0] < 3): Domoticz.Error("WARNING: Python3 should be used!")
          if (version_tuple(pymodbus.__version__) < (3, 0)): Domoticz.Error("WARNING: Pymodbus version is outdated (3.0 or newer is needed), please update!")
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

        # Currently in domoticz there is no way to add more parameters than Mode1 to Mode6, thus you need to modify this setting manually here.
        # "Yes" (same as the 2021.7 plugin): on a communication error the device is updated with '0'.
        # "No": on a communication error the device keeps its current state.
        self.Domoticz_Setting_Update_When_Error = "Yes"

        self.Domoticz_Setting_TCP_IPPORT = Parameters["Address"].split(":") # Split address and port setting TCP:IP
        self.Domoticz_Setting_TCP_IP = "0" # Default
        if len(self.Domoticz_Setting_TCP_IPPORT) > 0: self.Domoticz_Setting_TCP_IP = self.Domoticz_Setting_TCP_IPPORT[0]
        self.Domoticz_Setting_TCP_PORT = "502" # Default
        if len(self.Domoticz_Setting_TCP_IPPORT) > 1: self.Domoticz_Setting_TCP_PORT = self.Domoticz_Setting_TCP_IPPORT[1]

        # Set debug yes/no
        if (len(Domoticz_Setting_Communication_MODE) > 1 and Domoticz_Setting_Communication_MODE[1] == "debug"):
          Domoticz.Debugging(1) # Enable debugging
          DumpConfigToLog()
          Domoticz.Debug("***** NOTIFICATION: Debug enabled!")
        else:
          Domoticz.Debugging(0) # Disable debugging

        # RTU - Serial port settings: "S<stopbits>B<bytesize>P<parity>", e.g. S1B8PN
        self.StopBits, self.ByteSize, self.Parity = 1, 8, "N" # Default
        port_mode = self.Domoticz_Setting_Port_Mode
        if (len(port_mode) == 6 and port_mode[0] == "S" and port_mode[2] == "B" and port_mode[4] == "P"):
          self.StopBits, self.ByteSize, self.Parity = int(port_mode[1]), int(port_mode[3]), port_mode[5]

        if (len(Devices) == 0): Domoticz.Device(Name="ModbusWRITE", Unit=1, TypeName="Switch", Image=0, Used=1).Create() # Used=1 to add a switch immediatly!

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")
        return

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def UpdateWhenError(self):
        if (self.Domoticz_Setting_Update_When_Error == "Yes" and 1 in Devices):
          Devices[1].Update(1, "0") # Set value to 0 (error)

    def ConnectFailureReason(self):
        """connect() only returns False; find out why, so the Domoticz log says something useful."""
        mode = self.Domoticz_Setting_Communication_Mode
        if (mode == "rtu" or mode == "ascii"):
          port = self.Domoticz_Setting_Serial_Port
          if not os.path.exists(port): return "serial port " + port + " does not exist"
          if not os.access(port, os.R_OK | os.W_OK): return "no permission to open " + port + " (is the domoticz user in the 'dialout' group?)"
          return "could not open serial port " + port + " (in use by another program?)"
        target = self.Domoticz_Setting_TCP_IP + ":" + self.Domoticz_Setting_TCP_PORT
        try:
          test = socket.create_connection((self.Domoticz_Setting_TCP_IP, int(self.Domoticz_Setting_TCP_PORT)), timeout=3)
          test.close()
          return "a plain TCP connection to " + target + " works, but the device refused/dropped the Modbus client (many gateways allow only ONE connection at a time)"
        except OSError as e:
          return "TCP connection to " + target + " failed: " + str(e)

    def CreateClient(self):
        mode = self.Domoticz_Setting_Communication_Mode

        # pymodbus: RTU / ASCII (serial)
        if (mode == "rtu" or mode == "ascii"):
          Domoticz.Debug("MODBUS DEBUG - INTERFACE: Port="+self.Domoticz_Setting_Serial_Port+", BaudRate="+self.Domoticz_Setting_Baudrate+", StopBits="+str(self.StopBits)+", ByteSize="+str(self.ByteSize)+" Parity="+self.Parity)
          serial_args = dict(port=self.Domoticz_Setting_Serial_Port, baudrate=int(self.Domoticz_Setting_Baudrate), bytesize=self.ByteSize, parity=self.Parity, stopbits=self.StopBits, timeout=2, retries=2)
          try:
            takes_framer = "framer" in inspect.signature(ModbusSerialClient.__init__).parameters
          except Exception:
            takes_framer = True
          if takes_framer:
            return ModbusSerialClient(framer=FRAMERS[mode], **serial_args)
          return ModbusSerialClient(method=mode, **serial_args) # very old pymodbus 3.x: method="rtu"/"ascii"

        # pymodbus: RTU over TCP / TCP/IP
        Domoticz.Debug("MODBUS DEBUG - INTERFACE: IP="+self.Domoticz_Setting_TCP_IP+", Port="+self.Domoticz_Setting_TCP_PORT)
        framer = FRAMERS["rtu"] if mode == "rtutcp" else FRAMERS["socket"]
        return ModbusTcpClient(host=self.Domoticz_Setting_TCP_IP, port=int(self.Domoticz_Setting_TCP_PORT), framer=framer, timeout=2, retries=2)

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        # ON/OFF payload value
        payload = Level # Set payload from slider/scroll
        # Set payload if a button has been pressed
        if (str(Command) == "On"): payload = self.Domoticz_Setting_Payload_ON
        if (str(Command) == "Off"): payload = self.Domoticz_Setting_Payload_OFF

        mode = self.Domoticz_Setting_Communication_Mode
        Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+mode+", Device ID="+self.Domoticz_Setting_Device_ID+", Register="+self.Domoticz_Setting_Register_Number+", Function="+self.Domoticz_Setting_Modbus_Function+", Payload="+str(payload))

        ########################################
        # SET HARDWARE
        ########################################
        try:
          client = self.CreateClient()
        except Exception as e:
          Domoticz.Error("Error creating the Modbus interface (" + mode + "): " + str(e))
          self.UpdateWhenError()
          return

        ########################################
        # WRITE PAYLOAD
        ########################################
        try:
          if not client.connect():
            raise ConnectionError(self.ConnectFailureReason())

          address = int(self.Domoticz_Setting_Register_Number)
          device_id = int(self.Domoticz_Setting_Device_ID)
          function = self.Domoticz_Setting_Modbus_Function
          value = parse_payload(payload, PAYLOAD_BASE.get(mode, 10))

          # Function to execute
          if (function == "5"): result = client.write_coil(address, bool(value), **unit_kwargs(client.write_coil, device_id))
          elif (function == "6"): result = client.write_register(address, value, **unit_kwargs(client.write_register, device_id))
          elif (function == "15"): result = client.write_coils(address, [bool(value)], **unit_kwargs(client.write_coils, device_id))      # TODO split up multiple bytes to proper array.
          elif (function == "16"): result = client.write_registers(address, [value], **unit_kwargs(client.write_registers, device_id))  # TODO split up multiple bytes to proper array.
          else: raise ValueError("unknown Modbus function: " + str(function))

          if result.isError():
            raise IOError(str(result))
          Domoticz.Debug("MODBUS DEBUG - RESULT: " + str(result))
        except Exception as e:
          Domoticz.Error("Modbus error communicating! (" + mode + "), check your settings! (" + str(e) + ")")
          self.UpdateWhenError()
          return
        finally:
          try:
            client.close()
          except Exception:
            pass

        if (1 in Devices):
          if (str(Command) == "On"): Devices[1].Update(1, "1") # Update device to ON
          if (str(Command) == "Off"): Devices[1].Update(0, "0") # Update device to OFF

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        # Domoticz.Log("onHeartbeat called")
        return

    def UpdateDevice(self, Unit, nValue, sValue):
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
