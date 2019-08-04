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
<plugin key="Modbus2" name="Modbus device v1.0.0" author="B. Vreugdenhil. based on code by S. Ebeltjes / domoticx.nl" version="1.0.0" externallink="" wikilink="https://github.com/DomoticX/domoticz-modbus/">
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
	    <param field="Mode4" label="devicename" width="180px" required="true" value="Custom">
            <options>
                <option label="SDM220 din rail power meter" value="SDM220"/>
                <option label="2 Channel relay" value="twochannelrelay"/>
                <option label="Modbus5in5out" value="5In5Out"/>
                <option label="16ChannelCurrent" value="16ChannelCurrent"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
from modbusregister import ModbusRegister
import configparser
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
#data = []
reg = []
sTypeKwh = 0x1D
UnitAddress =1

class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        #if Parameters["Mode4"] == "debug":
        Domoticz.Debugging(1)
        #Domoticz.Debugging(0)	#Enable debugging by default, mode 4 is used for sensor mode
        
        #Removed the full name parameter
        
        Device=Parameters["Mode4"]
        Domoticz.Log("Device: "+Device)
        
        Domoticz.Log("Parameters[Address] "+Parameters["Address"])   
        # Split address to support TCP/IP device ID
        AddressData = Parameters["Address"].split("/") # Split on "/"
        UnitAddress = AddressData[0]
        Domoticz.Log("UnitAddress: "+str(UnitAddress))

        # Is there a unit ID given after the IP? (e.g. 192.168.2.100/56)
        self.UnitIdForIp = 1 # Default
        if len(AddressData) > 1:
            self.UnitIdForIp = AddressData[1]
            Domoticz.Log("UnitIdForIp: "+self.UnitIdForIp)      
        
        try:    
            filename= Parameters["HomeFolder"]+'modbusdevices.ini'
            config = configparser.ConfigParser()
            config.read_file(open(filename))
            numberofregisters=config[Device]['numberofregisters']

            Domoticz.Log("number of registers:"+numberofregisters)
           
            #if (len(Devices) <> numberofregisters):
            #    try:
            #        Devices[10].Delete()
            #        Devices[9].Delete()
            #        Devices[8].Delete()
            #        Devices[7].Delete() 
            #        Devices[6].Delete()
            #        Devices[5].Delete()
            #        Devices[4].Delete()
            #        Devices[3].Delete()
            #        Devices[2].Delete()
            #        Devices[1].Delete()
            #    except Exception as e:
            #        Domoticz.Log("Error deleting device "+repr(e))
           
            for x in range(1, int(numberofregisters)+1):
                tag=Device+'_reg_'
                Domoticz.Log("reg:" +str(x))
                function=config[Device+'_reg_'+str(x)]['function']
                reg_name=config[Device+'_reg_'+str(x)]['name']
                address=config[Device+'_reg_'+str(x)]['address']
                Sensortype=config[Device+'_reg_'+str(x)]['Sensortype']
                datatype=config[Device+'_reg_'+str(x)]['datatype']
                unitfallback=config['DEFAULT'][Sensortype]
                unit2=config.get(Device+'_reg_'+str(x),'unit',fallback=unitfallback)
                digits=config[Device+'_reg_'+str(x)]['digits']
                devide=config[Device+'_reg_'+str(x)]['devide']
                used=config[Device+'_reg_'+str(x)]['used']
                multiplydevice=config[Device+'_reg_'+str(x)]['multiply']
                Domoticz.Log("func:"+function+" name:"+reg_name+" adr:" +address+" sensortype:"+Sensortype+" datatype:"+datatype+" unit:"+unit2+" devide:"+devide+" digits:"+digits+" used="+used)
                if(unit2):
                    Domoticz.Log("unit true:"+unit2)
                else:    
                    Domoticz.Log("unit false:"+unit2)    
                Domoticz.Log("TypeName:"+Sensortype)
                
                #if Devices[x].TypeName<>Sensortype or (Sensortype=="kWh" and Devices[x].TypeName<>"Custom"):
                #    Devices[x].Delete()
                #    Domoticz.Log("Device Changed. TypeName:"+Sensortype) 
                
                if(x not in Devices):
                    if((Sensortype=="Custom") and unit2):
                        Options = { "Custom" : "1;"+unit2} 
                        Domoticz.Log("Custom with options:"+str(Options)+" unit:"+str(x))
                        Domoticz.Device(Name=reg_name, Unit=x,TypeName=Sensortype,Used=0,Options=Options).Create()
                    elif(Sensortype=="kWh")    :
                        Domoticz.Log("kwh:"+" unit:"+str(x))
                        Domoticz.Device(Name=reg_name, Unit=x,TypeName="Custom",Subtype=sTypeKwh,Used=0).Create()
                    else:   
                        Domoticz.Log("without options:"+" unit:"+str(x))
                        Domoticz.Device(Name=reg_name, Unit=x,TypeName=Sensortype,Used=0).Create()
                try:
                    #Domoticz.Log("step 1:"+str(x)+"Devices:"+str(len(Devices)))
                    Domoticz.Log("UnitAddress: "+str(UnitAddress)+"  device:"+Devices[x].sValue)
                    Domoticz.Log("step 2")
                    reg.append(ModbusRegister(function,address,datatype, devide,Sensortype,"",UnitAddress,Parameters["Mode1"],Devices[x],digits,multiplydevice))
                    #Domoticz.Log("step 3")
                    #Domoticz.Log("reg: created:"+str(x))
                except Exception as e:
                    Domoticz.Log("Error creating class "+repr(e))
                 
        except Exception as e:
            Domoticz.Log("Error opening config "+repr(e)+":"+filename)
        
        #Due to the lack of more parameter posibility, the name will be the hardware name
        #if (len(Devices) == 0):
        #   Domoticz.Device(Name=" ",  Unit=1, TypeName=Parameters["Mode4"], Image=0, Used=1).Create() #Added sensor type
        #if (len(Devices) == 1):        
        #   Domoticz.Device(Name=" ",  Unit=2, TypeName=Parameters["Mode4"], Image=0, Used=1).Create() #Added sensor type
        #if 3 not in Devices:
         #  Domoticz.Device(Name="Average Line To Neutral Volts", Unit=3,TypeName="Voltage",Used=0).Create()
        
        #try:
        #   reg.append(ModbusRegister(Parameters["Username"],int(Parameters["Password"]),Parameters["Mode6"], Parameters["Mode5"],Parameters["Mode4"],"",self.UnitIdForIp,Parameters["Mode1"],Devices[1]))
        #   reg.append( ModbusRegister(Parameters["Username"],31,Parameters["Mode6"], Parameters["Mode5"],Parameters["Mode4"],"",self.UnitIdForIp,Parameters["Mode1"],Devices[2]))
        #   Domoticz.Log("reg: created")
        #except Exception as e:
        #   Domoticz.Log("Error creating class "+repr(e))
        #Domoticz.Log("AFTER reg")
        
        #DumpConfigToLog()
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
        Domoticz.Log("onHeartbeat called")
       
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

        ###################################
        # pymodbus: RTU / ASCII
        ###################################
        if (Parameters["Mode1"] == "rtu" or Parameters["Mode1"] == "ascii"):
            Domoticz.Debug("MODBUS DEBUG USB SERIAL HW - Port="+Parameters["SerialPort"]+", BaudRate="+Parameters["Mode2"]+", StopBits="+str(StopBits)+", ByteSize="+str(ByteSize)+" Parity="+Parity)
            Domoticz.Debug("MODBUS DEBUG USB SERIAL CMD - Method="+Parameters["Mode1"])
            try:
                client = ModbusSerialClient(method=Parameters["Mode1"], port=Parameters["SerialPort"], stopbits=StopBits, bytesize=ByteSize, parity=Parity, baudrate=int(Parameters["Mode2"]), timeout=1, retries=2)
            except:
                Domoticz.Log("Error opening Serial interface on "+Parameters["SerialPort"])
                #Devices[1].Update(0, "0") # Update device in Domoticz

        ###################################
        # pymodbus: RTU over TCP
        ###################################
        if (Parameters["Mode1"] == "rtutcp"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"])
          try:
            client = ModbusTcpClient(host=UnitAddress, port=int(Parameters["Port"]), framer=ModbusRtuFramer, auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening TCP interface on address: "+UnitAddress)
            #Devices[1].Update(0, "0") # Update device in Domoticz

        ###################################
        # pymodbusTCP: TCP/IP
        ###################################
        if (Parameters["Mode1"] == "tcpip"):
          Domoticz.Debug("MODBUS DEBUG TCP CMD - Method="+Parameters["Mode1"]+", Address="+UnitAddress+", Port="+Parameters["Port"]+", Unit ID="+self.UnitIdForIp+", Register="+Parameters["Password"]+", Data type="+Parameters["Mode6"])
          try:
            client = ModbusClient(host=UnitAddress, port=int(Parameters["Port"]), unit_id=self.UnitIdForIp, auto_open=True, auto_close=True, timeout=5)
          except:
            Domoticz.Log("Error opening TCP/IP interface on address: "+UnitAddress)
            #Devices[1].Update(0, "0") # Update device in Domoticz
        try:
            #Domoticz.Log("Before update. Number of devices:"+str(len(Devices)))
            for i in reg:
                i.update(client,Domoticz)
            #Domoticz.Log("After update")
        except Exception as e:
            Domoticz.Log("Error calling update "+repr(e))
           
        client.close()
        
    def UpdateDevice(Unit, nValue, sValue):
        # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
        if (Unit in Devices):
            #if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or Devices[Unit].LastUpdate>5:
            if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
                Devices[Unit].Update(nValue, str(sValue))
                Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
            #else:
            #    Domoticz.Log("no update "+str(nValue)+" Lastupdate:"+str(Devices[Unit].LastUpdate)) 
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
