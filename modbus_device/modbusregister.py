from pymodbus.constants import Endian   
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer
import Domoticz
from datetime import datetime
import time

data = []

class  ModbusRegister:
    
    def __init__(self, function, address,dataType,devide,sensorType, unit,UnitIdForIp,method,device, digits=8,multiplydevice):
        #Domoticz.Log("__init called")
        self.function = function
        self.address = int(address)
        self.dataType = dataType
        self.device = device
        if devide<>"":
            self.devide=devide[4:]
        if self.devide=0 or self.devide="": self.devide = 1    
        
        self.devide = devide
        self.sensorType = sensorType
        self.unit = unit
        self.UnitIdForIp = int(UnitIdForIp)
        self.method = method
        self.digits=int(digits)
        self.multiplydevice=multiplydevice
        swapped = False
       
        #Domoticz.Log("1 called")
        if (dataType == "int16" or dataType == "uint16") and swapped: 
            self.byteorder=Endian.Little
            self.wordorder=Endian.Big         
        elif (dataType == "int32s" or dataType == "uint32s" or dataType == "int64s" or dataType == "uint64s" 
             or dataType == "float32s" or dataType == "float64s"):
            self.byteorder=Endian.Big
            self.wordorder=Endian.Little
        # Otherwise always big endian
        else:
            self.byteorder=Endian.Big
            self.wordorder=Endian.Big
        #Domoticz.Log("2 called")
       
        self.swapped= dataType[-1:] == "s"
        if(self.dataType[-1:]== 's'):
            self.dataType = self.dataType[:-1]
        #self.client = client
        #Domoticz.Log("3 called")
        
        # How many registers to read (depending on data type)?
	    # Added additional options for byte/word swapping
        self.registercount = 1 # Default
        if (dataType == "noco"): self.registercount = 1
        if (dataType == "int8LSB"): self.registercount = 1
        if (dataType == "int8MSB"): self.registercount = 1
        if (dataType == "int16"): self.registercount = 1
        if (dataType == "int32"): self.registercount = 2
        if (dataType == "int64"): self.registercount = 4
        if (dataType == "uint8LSB"): self.registercount = 1
        if (dataType == "uint8MSB"): self.registercount = 1
        if (dataType == "uint16"): self.registercount = 1
        if (dataType == "uint32"): self.registercount = 2
        if (dataType == "uint64"): self.registercount = 4
        if (dataType == "float32"): self.registercount = 2
        if (dataType == "float64"): self.registercount = 4
        if (dataType == "string2"): self.registercount = 2
        if (dataType == "string4"): self.registercount = 4
        if (dataType == "string6"): self.registercount = 6
        if (dataType == "string8"): self.registercount = 8
        #self.device.Update(0, "0")
    
    def update(self,client,Domoticz):
        value = "0"
        
        #Domoticz.Log("--> Device:"+self.device.Name+" Address="+str(self.UnitIdForIp)+", Register="+str(self.address)+", Function="+self.function+", Data type="+self.dataType+" Digits:"+str(self.digits)+" Method="+self.method)
        ###################################
        # pymodbus section
        ###################################
         
        if (self.method == "rtu" or self.method == "ascii" or self.method == "rtutcp"):
            Domoticz.Log("Start rtu read")
            
            try:
                # Which function to execute? RTU/ASCII/RTU over TCP or COM
                if (self.function == "1"): data = client.read_coils(self.address, self.registercount, unit=self.UnitIdForIpUnitIdForIp)
                elif (self.function == "2"): data = client.read_discrete_inputs(self.address, self.registercount, unit=self.UnitIdForIp)
                elif (self.function == "3"): data = client.read_holding_registers(self.address, self.registercount, unit=self.UnitIdForIp)
                elif (self.function == "4"): data = client.read_input_registers(self.address, self.registercount, unit=self.UnitIdForIp)
                else:
                    Domoticz.Debug("No function selected: " + str(self.function))
                    return
                Domoticz.Log("MODBUS DEBUG RESPONSE: " + str(data.registers))
            except Exception as e:
                Domoticz.Log("Modbus error communicating! (RTU/ASCII/RTU over TCP or COM), check your settings!"+repr(e))
                data = 0
                #self.device.Update(0, "0") # Update device to OFF in Domoticz

        ###################################
        # pymodbusTCP section
        ###################################
        else:  #if (self.method == "tcpip"):
            #Domoticz.Log("Start tcp read")
            
            try:
                # Which function to execute? TCP/IP
                if (function == "1"): data = client.read_coils(self.address, self.registercount)
                if (function == "2"): data = client.read_discrete_inputs(self.address, self.registercount)
                if (function == "3"): data = client.read_holding_registers(self.address, self.registercount)
                if (function == "4"): data = client.read_input_registers(self.address, self.registercount)
                Domoticz.Log("MODBUS DEBUG RESPONSE: " + str(data))
            except Exception as e:
                Domoticz.Log("Modbus error communicating! (TCP/IP), check your settings!"+repr(e))
                data = 0 
                #self.device.Update(0, "0") # Update device to OFF in Domoticz

        #Domoticz.Log("Modbus Na read" )
        
        if data:
            try:
                # How to decode the input?
                try:
                    decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=self.byteorder, wordorder=self.wordorder)
                except:            
                    decoder = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=self.byteorder, wordorder=self.wordorder)
            
                if (self.dataType == "noco"): value = data
                if (self.dataType == "int8LSB"):
                    ignored = decoder.skip_bytes(1)
                    value = decoder.decode_8bit_int()
                if (self.dataType == "int8MSB"): value = decoder.decode_8bit_int()
                if (self.dataType == "int16"): value = decoder.decode_16bit_int()
                if (self.dataType == "int16s"): value = decoder.decode_16bit_int()
                if (self.dataType == "int32"): value = decoder.decode_32bit_int()
                if (self.dataType == "int64"): value = decoder.decode_64bit_int()
                if (self.dataType == "uint8LSB"):
                    ignored = decoder.skip_bytes(1)
                    value = decoder.decode_8bit_uint()
                if (self.dataType == "uint8MSB"): value = decoder.decode_8bit_uint()   
                if (self.dataType == "uint16"): value = decoder.decode_16bit_uint()
                if (self.dataType == "uint32"): value = decoder.decode_32bit_uint()
                if (self.dataType == "uint64"): value = decoder.decode_64bit_uint()
                if (self.dataType == "float32"): value = decoder.decode_32bit_float()
                if (self.dataType == "float64"): value = decoder.decode_64bit_float()
                if (self.dataType == "string2"): value = decoder.decode_string(2)
                if (self.dataType == "string4"): value = decoder.decode_string(4)
                if (self.dataType == "string6"): value = decoder.decode_string(6)
                if (self.dataType == "string8"): value = decoder.decode_string(8)
                if (self.dataType == "bcd8"):
                    value=decoder.decoder.decode_8bit_int()
                    value=value & 0xf + value & (0xf0&0xf0>>4*10)
                if (self.dataType == "bcd16"):
                    value=decoder.decoder.decode_8bit_int()
                    value=value & 0xf + (value & 0xf0>>4*10) + (value & 0xf00>>8*100) + (value & 0xf000>>12*1000)
                if multiplydevice:
                   value=value*domoticz.device(multiplydevice)

                # Divide the value (decimal)?
                value = str(round(value / self.devide, self.digits))
                
                Domoticz.Log("MODBUS DEBUG VALUE: " + str(value)+" Old value:"+self.device.sValue+" Old value:"+str(self.device.nValue))
                #Domoticz.Log("LastUpdate:"+self.device.LastUpdate)
                
                age=(datetime.now()-datetime.strptime(self.device.LastUpdate, '%Y-%m-%d %H:%M:%S')).seconds
                
                #Domoticz.Log("LastUpdate seconds ago:"+str(age))
                if (self.device.sValue != value ) or age>300:
                    self.device.Update(0, value) # Update value in Domoticz
                    #Domoticz.Debug("Done update: " + str(value))
                    
                
            except Exception as e:
                Domoticz.Log("Modbus error decoding or received no data (TCP/IP)!, check your settings!"+repr(e))
                #self.device.Update(0, "0") # Update value in Domoticz
        else:       
            Domoticz.Log("No data")
                