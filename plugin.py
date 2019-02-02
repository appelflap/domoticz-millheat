# Millheat Python Plugin for Domoticz
#
# Author: Appelflap (Albert Drenth) <albert@appelflap.me>
#
"""
<plugin key="MillHeat" name="MillHeat Control" author="appelflap" version="0.1.4" externallink="https://github.com/appelflap/domoticz-millheat">
    <description>
        <h2>MillHeat Plugin</h2>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Automatically makes devices for your heaters</li>
        </ul>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Heater - On/Off</li>
            <li>Thermostat - Thermostat temperature setpoint</li>
            <li>Power - Percentage</li>
            <li>Status - String</li>
            <li>Alarm - On/Off (read-only)</li>
        </ul>
        <h3>Configuration</h3>
    </description>
    <params>
        <param field="Username" label="Email" width="250px" required="true" default=""/>
        <param field="Password" label="Password" width="250px" required="true" default=""/>
        <param field="Mode1" label="Check Interval(seconds)" width="75px" required="true" default="60"/>
        <param field="Mode2" label="Notifications" width="75px">
            <options>
                <option label="Notify" value="Notify"/>
                <option label="Disable" value="Disable" default="true" />
            </options>
        </param>
        <param field="Mode6" label="Debug" width="100px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import sys
import getpass
import threading
import site
import os

path=''
path=site.getsitepackages()
for i in path:    
    sys.path.append(i)

import mill

# import fakeDomoticz as Domoticz
# Parameters = {'Username':'myusername', 'Password':'mypassword', 'Mode1':'60', 'Mode2': 'Notify', 'Mode6': 'Debug'}
# Settings = {}
# Devices = {}
# class Image:
    # ID = 1
# Images = {'Fireplace': Image}

class MillHeat:
    notify = False
    debug = False
    
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        
        self.pollInterval = int(Parameters["Mode1"])  #Time in seconds between two polls
                
        if Parameters["Mode2"] == "Notify":
            self.notify = True

        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            self.debug = True
            DumpConfigToLog()
                
        Domoticz.Heartbeat(self.pollInterval)
        
        self.mill = mill.Mill(Parameters["Username"], Parameters["Password"])
        self.mill.sync_connect()
        self.mill.sync_update_heaters()
        
        self.getDevices()

    def onStop(self):
        Domoticz.Log("Plugin is stopping")
        Domoticz.Debugging(0)
        Domoticz.Log("Threads still active: "+str(threading.active_count())+", should be 1.")
        while (threading.active_count() > 1):
            for thread in threading.enumerate():
                if (thread.name != threading.current_thread().name):
                    Domoticz.Log("'"+thread.name+"' is still running, waiting otherwise Domoticz will crash on plugin exit.")
            time.sleep(1.0)


    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            Domoticz.Debug("MillHeat connected successfully")
            sendData = { 'Verb': 'POST', 'URL': self.url, 'Headers': self.headers}
            Connection.Send(sendData) # Jumps to onMessage
        else:
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["Address"]+":"+Parameters["Mode1"]+" with error: "+Description)


    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        
        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.capitalize()

        self.mill = mill.Mill(Parameters["Username"], Parameters["Password"])
        self.mill.sync_connect()
        self.mill.sync_update_heaters()
        
        Domoticz.Debug("Action = "+action)
        
        if (action == 'On'):
            if (Devices[Unit].Type == 244):
                Domoticz.Log("Turning Switch "+Devices[Unit].DeviceID+" (external: "+str(decodeHeaterId(Devices[Unit].DeviceID[0:4]))+") On!")
                self.mill.sync_heater_control(decodeHeaterId(Devices[Unit].DeviceID[0:4]), fan_status=0, power_status=1)        
        if (action == 'Off'):
            if (Devices[Unit].Type == 244):
                Domoticz.Log("Turning Switch "+Devices[Unit].DeviceID+" (external: "+str(decodeHeaterId(Devices[Unit].DeviceID[0:4]))+") Off!")
                self.mill.sync_heater_control(decodeHeaterId(Devices[Unit].DeviceID[0:4]), fan_status=0, power_status=0)
        if (action == 'Set'):
            if (Devices[Unit].Type==242):
                Domoticz.Log("Setting Thermostat "+Devices[Unit].DeviceID+" (external: "+str(decodeHeaterId(Devices[Unit].DeviceID[0:4]))+") to "+str(Level))
                self.mill.sync_set_heater_temp(decodeHeaterId(Devices[Unit].DeviceID[0:4]), round(Level))

        self.getDevices()
                
        self.mill.sync_close_connection()
                        
    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        
        self.mill = mill.Mill(Parameters["Username"], Parameters["Password"])
        self.mill.sync_connect()
        
        # Do some stuffff
        self.getDevices()
        
        Domoticz.Heartbeat(self.pollInterval)

        self.mill.sync_close_connection()
        
    def getDevices(self):
        self.heaterIdList=dev2id()
        
        self.mill.sync_update_heaters()

        myHeaters = {}
        for heater in iter(self.mill.heaters.values()):
            myHeaters[encodeHeaterId(heater.device_id)] = heater
            # self.mill.sync_set_heater_temp(heater.device_id, 11)
            # self.mill.sync_set_heater_control(heater.device_id, fan_status=0)

        self.syncDevices(myHeaters)
        
    
    def syncDevices(self, myHeaters):
        Domoticz.Log("createDevices called")

        for heaterId in myHeaters:
            dumpHeater(myHeaters[heaterId])
            if heaterId+str(1) not in self.heaterIdList:
                Domoticz.Device(Name=myHeaters[heaterId].name+" Status", Unit=firstFree(), DeviceID=heaterId+str(1), TypeName="Switch", Used=1).Create() # Image=Images["Fireplace"].ID
            if heaterId+str(2) not in self.heaterIdList:
                Domoticz.Device(Name=myHeaters[heaterId].name+" Temperature", Unit=firstFree(), DeviceID=heaterId+str(2), TypeName="Temperature", Used=1).Create()
            if heaterId+str(3) not in self.heaterIdList:
                Domoticz.Device(Name=myHeaters[heaterId].name+" Thermostat", Unit=firstFree(), DeviceID=heaterId+str(3), Type=242, Subtype=1, Used=1).Create()
        
            # Also index just created devices
            self.heaterIdList=dev2id()
        
            # Update the values
            UpdateDevice(Devices[self.heaterIdList[heaterId+str(1)]].Unit, 0, str(myHeaters[heaterId].is_heating))
            UpdateDevice(Devices[self.heaterIdList[heaterId+str(2)]].Unit, 0, str(round(myHeaters[heaterId].current_temp, 1)))
            UpdateDevice(Devices[self.heaterIdList[heaterId+str(3)]].Unit, 0, str(round(myHeaters[heaterId].set_temp, 1)))
     
        # Index those values
        self.heaterIdList=dev2id()
    
        #find and remove obsolete devices
        obsolete=[]
        for check in Devices:
            if Devices[check].DeviceID[0:4] not in myHeaters:
                obsolete.append(check)
        for trash in obsolete:
            Domoticz.Log("Removing Mill Heater " + str(Devices[trash].ID) + " " + str(Devices[trash].Name) + " (obsolete).")
            Devices[trash].Delete()
            
        self.heaterIdList=dev2id()
     
    #
    # Parse an int and return None if no int is given
    #

    def parseIntValue(self, s):

        try:
            return int(s)
        except:
            return None

    #
    # Parse a float and return None if no float is given
    #

    def parseFloatValue(self, s):

        try:
            return float(s)
        except:
            return None
    
global _plugin
_plugin = MillHeat()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

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

#map heaterId (external) to internal Domoticz ID's
def dev2id():
    devlist={}
    for thing in Devices:
        devlist[Devices[thing].DeviceID]=thing
        Domoticz.Debug("Indexing device 'DeviceID=" + Devices[thing].DeviceID + ", Name="+Devices[thing].Name+", Unit="+str(Devices[thing].Unit)+", ID="+str(Devices[thing].ID)+", Type="+str(Devices[thing].Type)+"' to the devlist")
    return devlist
    
#find the first available (internal) unit id
def firstFree():
    for num in range(1,250):
        if num not in Devices:
            return num
    return
    
def encodeHeaterId(realid):
    if int(realid)==-1:
        #results in FFFFFFFF hex
        return format(4294967295, 'X')
    else:
        return format(int(realid), 'X')
        
def decodeHeaterId(fakeid):
    if fakeid==4294967295:
        return -1
    else:
        return int(fakeid, 16)

def dumpHeater(heater):
    Domoticz.Debug('Heater {} (name={}, device_id={},' \
           ' current_temp={}, set_temp={},'\
           ' power_status={}, is_heating={})'.format(encodeHeaterId(heater.device_id), 
                                                   heater.name,
                                                   heater.device_id,
                                                   heater.current_temp,
                                                   heater.set_temp,
                                                   heater.power_status,
                                                   heater.is_heating
                                                   ))
    
# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Settings count: " + str(len(Settings)))
    for x in Settings:
        Domoticz.Debug( "'" + x + "':'" + str(Settings[x]) + "'")
    Domoticz.Debug("Image count: " + str(len(Images)))
    for x in Images:
        Domoticz.Debug( "'" + x + "':'" + str(Images[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
        Domoticz.Debug("Device Image:     " + str(Devices[x].Image))
    return
    
# Update Device into database
def UpdateDevice(Unit, nValue, sValue, AlwaysUpdate=False):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != sValue or AlwaysUpdate == True:
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update " + Devices[Unit].Name + ": " + str(nValue) + " - '" + str(sValue) + "'")
    return
