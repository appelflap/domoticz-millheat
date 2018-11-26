class dummyDevice:
    def __init__(self, Name="", Unit=0, Type=0, Subtype=0, TypeName="", Used=1, DeviceID = "", Image = 0):
        self.Name = Name
        self.Unit = Unit
        self.Type = Type
        self.Subtype = Subtype
        self.TypeName = TypeName
        self.Used = Used
        self.DeviceID = DeviceID
        self.Image = Image
        return
        
    def Create(self):
        print("Create Device... With name:"+self.Name)

def Log(s):
    print(s)

def Debug(s):
    print(s)

def Error(s):
    print(s)
    
def Debugging(s):
    print(s)
    
def Heartbeat(s):
    print("Starting heartbeat in "+str(s)+" seconds")
    
def Device(Name="", Unit=0, Type=0, Subtype=0, TypeName="", Used=1, DeviceID = "", Image = 0):
    newDevice = dummyDevice(Name,Unit, Type, Subtype, TypeName, Used, DeviceID, Image)
    return newDevice

