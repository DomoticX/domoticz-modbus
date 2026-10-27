# Modbus RTU / ASCII / TCP/IP - Universal READ Plugin for Domoticz
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
# - values are decoded with struct instead of the deprecated BinaryPayloadDecoder / Endian
# - fixed scale factors "mul100/mul1000/mul10000" (they raised an error) and the "mull10000" typo
# - fixed coil / discrete input reads and string decoding
# - connection errors now say why the connection failed
#
# Dependancies:
# - pymodbus:
#   - Install for python3 with: sudo pip3 install -U pymodbus   (3.6.9 up to 3.8.x are supported)
#     (use a virtual environment or --break-system-packages if your distro blocks pip)
# - pyModbusTCP is NOT needed anymore
#
"""
<plugin key="ModbusREAD" name="Modbus RTU / ASCII / TCP/IP - READ v2026.4" author="S. Ebeltjes / DomoticX.nl" version="2026.4" externallink="http://domoticx.nl" wikilink="https://github.com/DomoticX/domoticz-modbus">
    <description>
        <h3>Modbus RTU / ASCII / TCP/IP - READ</h3>
        With this plugin you can read from RS485 Modbus devices with methods RTU/ASCII/TCP<br/>
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
        <param field="Password" label="Device ID(decimal):Pollingrate(sec)" width="50px" default="1:10" required="true"/>
        <param field="Username" label="Modbus Function" width="250px" required="true">
            <options>
                <option label="Read Coil (Function 1)" value="1"/>
                <option label="Read Discrete Input (Function 2)" value="2"/>
                <option label="Read Holding Registers (Function 3)" value="3" default="true"/>
                <option label="Read Input Registers (Function 4)" value="4"/>
            </options>
        </param>
        <param field="Port" label="Register number(decimal)" width="50px" default="1" required="true"/>
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
                <option label="FLOAT 32-Bit Swapped" value="float32s"/>
                <option label="FLOAT 64-Bit" value="float64"/>
                <option label="FLOAT 64-Bit Swapped" value="float64s"/>
                <option label="STRING 2-byte" value="string2"/>
                <option label="STRING 4-byte" value="string4"/>
                <option label="STRING 6-byte" value="string6"/>
                <option label="STRING 8-byte" value="string8"/>
            </options>
        </param>
        <param field="Mode5" label="Scale factor" width="180px" required="true">
            <options>
                <option label="None" value="div0" default="true"/>
                <option label="Divide / 10" value="div10"/>
                <option label="Divide / 100" value="div100"/>
                <option label="Divide / 1000" value="div1000"/>
                <option label="Divide / 10000" value="div10000"/>
                <option label="Multiply * 10" value="mul10"/>
                <option label="Multiply * 100" value="mul100"/>
                <option label="Multiply * 1000" value="mul1000"/>
                <option label="Multiply * 10000" value="mul10000"/>
                <option label="In next register" value="sfnextreg"/>
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
import os
import sys
import socket
import struct
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


# Data types: name -> (struct format, number of 16-bit registers)
NUMERIC_TYPES = {
    "int16":   ("h", 1), "uint16":  ("H", 1),
    "int32":   ("i", 2), "uint32":  ("I", 2),
    "int64":   ("q", 4), "uint64":  ("Q", 4),
    "float32": ("f", 2), "float64": ("d", 4),
}

# Data types that need more than one register, or one register: see BasePlugin.onStart
REGISTER_COUNT = {
    "noco": 1, "bool": 1,
    "int8LSB": 1, "int8MSB": 1, "uint8LSB": 1, "uint8MSB": 1,
    "int16": 1, "int16s": 1, "uint16": 1, "uint16s": 1,
    "int32": 2, "int32s": 2, "uint32": 2, "uint32s": 2,
    "int64": 4, "int64s": 4, "uint64": 4, "uint64s": 4,
    "float32": 2, "float32s": 2, "float64": 4, "float64s": 4,
    "string2": 2, "string4": 4, "string6": 6, "string8": 8,
}


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


def decode_registers(registers, data_type):
    """Decode a list of 16-bit register values (big endian on the wire) to a python value.

    Replaces the deprecated BinaryPayloadDecoder, with identical results:
      - "...s" 16-bit types : the two bytes of the register are swapped
      - "...s" 32/64-bit types: the order of the 16-bit words is reversed
      - 8-bit LSB types     : low byte of the register, MSB types: high byte
    """
    if data_type == "noco":
        return registers[0]
    if data_type == "bool":
        return bool(registers[0])

    if data_type in ("int8LSB", "uint8LSB", "int8MSB", "uint8MSB"):
        byte = (registers[0] & 0xFF) if data_type.endswith("LSB") else ((registers[0] >> 8) & 0xFF)
        if data_type.startswith("int") and byte > 127:
            byte -= 256
        return byte

    if data_type.startswith("string"):
        size = int(data_type[6:])
        raw = b"".join(struct.pack(">H", r) for r in registers)[:size]
        return raw.decode("ascii", errors="replace").replace("\x00", "").strip()

    swapped = data_type.endswith("s")
    base = data_type[:-1] if swapped else data_type
    fmt, words = NUMERIC_TYPES[base]
    regs = list(registers[:words])
    if len(regs) < words:
        raise ValueError("received " + str(len(regs)) + " registers, need " + str(words))
    if swapped:
        if words == 1:
            regs = [((r & 0xFF) << 8) | (r >> 8) for r in regs]  # swap bytes
        else:
            regs.reverse()                                       # swap words
    return struct.unpack(">" + fmt, b"".join(struct.pack(">H", r) for r in regs))[0]


def apply_scale(value, scale, sf_value):
    """Apply the chosen scale factor and return the value as a string for Domoticz."""
    if isinstance(value, str):
        return value
    if scale == "div10": return str(round(value / 10, 1))
    if scale == "div100": return str(round(value / 100, 2))
    if scale == "div1000": return str(round(value / 1000, 3))
    if scale == "div10000": return str(round(value / 10000, 4))
    if scale == "mul10": return str(value * 10)
    if scale == "mul100": return str(round(value * 100, 2))
    if scale == "mul1000": return str(round(value * 1000, 3))
    if scale in ("mul10000", "mull10000"): return str(round(value * 10000, 4)) # "mull10000" = old (misspelled) saved setting
    if scale == "sfnextreg":
        if sf_value == 0: return str(value)
        if sf_value == 1: return str(round(value * 10, 1))
        if sf_value == 2: return str(round(value * 100, 1))
        if sf_value == -1: return str(round(value / 10, 1))
        if sf_value == -2: return str(round(value / 100, 1))
        return str(round(value * (10 ** sf_value), max(0, -sf_value))) # other scale factors
    return str(value) # "div0" = none


class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        try:
          Domoticz.Log("Modbus RTU/ASCII/TCP - Universal READ loaded!, using python v" + sys.version.split()[0] + " and pymodbus v" + pymodbus.__version__)
        except:
          Domoticz.Log("Modbus RTU/ASCII/TCP - Universal READ loaded!")

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

        Domoticz_Setting_Communication_MODDEB = Parameters["Mode1"].split(":") # Split MODE and DEBUG setting MODE:DEBUG
        self.Domoticz_Setting_Communication_Mode = Domoticz_Setting_Communication_MODDEB[0]
        self.Domoticz_Setting_Serial_Port = Parameters["SerialPort"]
        self.Domoticz_Setting_Baudrate = Parameters["Mode2"]
        self.Domoticz_Setting_Port_Mode = Parameters["Mode3"]
        self.Domoticz_Setting_Modbus_Function = Parameters["Username"]
        self.Domoticz_Setting_Register_Number = Parameters["Port"]
        self.Domoticz_Setting_Data_Type = Parameters["Mode6"]
        self.Domoticz_Setting_Scale_Factor = Parameters["Mode5"]
        self.Domoticz_Setting_Sensor_Type = Parameters["Mode4"]

        # Currently in domoticz there is no way to add more parameters than Mode1 to Mode6, thus you need to modify this setting manually here.
        # "No": on a communication/decoding error the device keeps its last value.
        # "Yes": on a communication/decoding error the device is updated with '0'.
        self.Domoticz_Setting_Update_When_Error = "No"

        self.Domoticz_Setting_Device_IDPOL = Parameters["Password"].split(":") # Split ID and pollrate setting ID:POLL (heartbeat)
        self.Domoticz_Setting_Device_ID = "1" # Default
        if len(self.Domoticz_Setting_Device_IDPOL) > 0: self.Domoticz_Setting_Device_ID = self.Domoticz_Setting_Device_IDPOL[0]
        self.Domoticz_Setting_Device_Pollrate = "10" # Default
        if len(self.Domoticz_Setting_Device_IDPOL) > 1: self.Domoticz_Setting_Device_Pollrate = self.Domoticz_Setting_Device_IDPOL[1]

        self.Domoticz_Setting_TCP_IPPORT = Parameters["Address"].split(":") # Split address and port setting TCP:IP
        self.Domoticz_Setting_TCP_IP = "0" # Default
        if len(self.Domoticz_Setting_TCP_IPPORT) > 0: self.Domoticz_Setting_TCP_IP = self.Domoticz_Setting_TCP_IPPORT[0]
        self.Domoticz_Setting_TCP_PORT = "502" # Default
        if len(self.Domoticz_Setting_TCP_IPPORT) > 1: self.Domoticz_Setting_TCP_PORT = self.Domoticz_Setting_TCP_IPPORT[1]

        # Set debug yes/no
        if (len(Domoticz_Setting_Communication_MODDEB) > 1 and Domoticz_Setting_Communication_MODDEB[1] == "debug"):
          Domoticz.Debugging(1) # Enable debugging
          DumpConfigToLog()
          Domoticz.Debug("***** NOTIFICATION: Debug enabled!")
        else:
          Domoticz.Debugging(0) # Disable debugging

        # Set device pollrate (heartbeat)
        Domoticz.Heartbeat(int(self.Domoticz_Setting_Device_Pollrate))
        Domoticz.Debug("***** NOTIFICATION: Pollrate (heartbeat): "+self.Domoticz_Setting_Device_Pollrate+" seconds.")

        # RTU - Serial port settings: "S<stopbits>B<bytesize>P<parity>", e.g. S1B8PN
        self.StopBits, self.ByteSize, self.Parity = 1, 8, "N" # Default
        port_mode = self.Domoticz_Setting_Port_Mode
        if (len(port_mode) == 6 and port_mode[0] == "S" and port_mode[2] == "B" and port_mode[4] == "P"):
          self.StopBits, self.ByteSize, self.Parity = int(port_mode[1]), int(port_mode[3]), port_mode[5]

        # Read n registers depending on data type (the "...s" types are the byte/word swapped variants)
        self.Register_Count = REGISTER_COUNT.get(self.Domoticz_Setting_Data_Type, 1)

        self.Read_Scale_Factor = 0
        if (self.Domoticz_Setting_Scale_Factor == "sfnextreg"):
          self.Read_Scale_Factor = 1
          self.Register_Count = self.Register_Count + 1

        # Coils and discrete inputs are single bits: always read exactly one, scale factor register does not apply
        if (self.Domoticz_Setting_Modbus_Function in ("1", "2")):
          self.Register_Count = 1
          self.Read_Scale_Factor = 0

        # Due to the lack of more parameter posibility, the name will be the hardware name
        self.Domoticz_Setting_Sensor_Type = Parameters["Mode4"]
        if (len(Devices) == 0): Domoticz.Device(Name="Modbus-READ",  Unit=1, TypeName=self.Domoticz_Setting_Sensor_Type, Image=0, Used=1).Create() #Added sensor type

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

    def UpdateWhenError(self):
        if (self.Domoticz_Setting_Update_When_Error == "Yes"):
          Domoticz.Log("Error reading value, still updating with '0' ")
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

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        Domoticz.Debug("MODBUS DEBUG - SETTINGS: Method="+self.Domoticz_Setting_Communication_Mode+", Device ID="+self.Domoticz_Setting_Device_ID+", Register="+self.Domoticz_Setting_Register_Number+", Function="+self.Domoticz_Setting_Modbus_Function+", Data type="+self.Domoticz_Setting_Data_Type+", Pollrate="+self.Domoticz_Setting_Device_Pollrate)

        ########################################
        # SET HARDWARE
        ########################################
        try:
          client = self.CreateClient()
        except Exception as e:
          Domoticz.Error("Error creating the Modbus interface (" + self.Domoticz_Setting_Communication_Mode + "): " + str(e))
          self.UpdateWhenError()
          return

        try:
          ########################################
          # GET DATA
          ########################################
          if not client.connect():
            raise ConnectionError(self.ConnectFailureReason())

          address = int(self.Domoticz_Setting_Register_Number)
          count = self.Register_Count
          device_id = int(self.Domoticz_Setting_Device_ID)
          function = self.Domoticz_Setting_Modbus_Function

          # pymodbus 3.x: unit= was replaced by slave= (named device_id in the newest releases)
          unit_kwargs = {"slave": device_id}
          try:
            params = inspect.signature(client.read_holding_registers).parameters
            for name in ("device_id", "slave", "unit"):
              if name in params:
                unit_kwargs = {name: device_id}
                break
          except Exception:
            pass

          if (function == "1"): response = client.read_coils(address, count=count, **unit_kwargs)
          elif (function == "2"): response = client.read_discrete_inputs(address, count=count, **unit_kwargs)
          elif (function == "3"): response = client.read_holding_registers(address, count=count, **unit_kwargs)
          elif (function == "4"): response = client.read_input_registers(address, count=count, **unit_kwargs)
          else: raise ValueError("unknown Modbus function: " + str(function))

          if response.isError():
            raise IOError(str(response))

          if (function in ("1", "2")):
            data = list(response.bits[:1])
          else:
            data = list(response.registers)
          Domoticz.Debug("MODBUS DEBUG - RESPONSE: " + str(data))
        except Exception as e:
          Domoticz.Error("Modbus error communicating! (" + self.Domoticz_Setting_Communication_Mode + "), check your settings! (" + str(e) + ")")
          self.UpdateWhenError()
          return
        finally:
          try:
            client.close()
          except Exception:
            pass

        ########################################
        # DECODE DATA VALUE
        ########################################
        try:
          sf_value = 0
          if (self.Read_Scale_Factor == 1):
            # The last register holds the (signed 16-bit) scale factor
            sf_value = struct.unpack(">h", struct.pack(">H", data[self.Register_Count - 1]))[0]
            data = data[0:self.Register_Count - 1]

          Domoticz.Debug("MODBUS DEBUG - VALUE before conversion: " + str(data))
          if (self.Domoticz_Setting_Modbus_Function in ("1", "2")):
            value = bool(data[0]) if (self.Domoticz_Setting_Data_Type == "bool") else int(data[0])
          else:
            value = decode_registers(data, self.Domoticz_Setting_Data_Type)

          # Apply a scale factor (decimal)
          value = apply_scale(value, self.Domoticz_Setting_Scale_Factor, sf_value)
          Domoticz.Debug("MODBUS DEBUG - VALUE after conversion: " + str(value))
          Devices[1].Update(1, value) # Update value

        except Exception as e:
          Domoticz.Error("Modbus error decoding or received no data!, check your settings! (" + str(e) + ")")
          self.UpdateWhenError()

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
