# domoticz-millheat
Domoticz MillHeat Plugin

Work in progress! 

Short summary
-------------

Add virtual devices for your MillHeat devices to your [Domoticz](https://www.domoticz.com/)

Get full device status from the API into your Domoticz
Current info:
* On/Off status
* Temperature
* Thermostat Setpoint

Able to change:
* Thermostat Setpoint

Installation and setup
----------------------

If you are use a Raspberry Pi to host your Domoticz, you probably need to install some python stuff for plugin to work.

```bash
sudo apt install python3-dev python3-pip
pip3 install millheater
# or sometimes:
python3 -m pip install millheater
# Sometimes you need to upgrade pip3 to get the right packages:
pip3 install --upgrade pip
```

Link the local dir to subdir.. otherwise we can't find it.. 
```bash
ln -s ~/.local/lib/python3.5/site-packages packages
```

In your `domoticz/plugins` directory do

```bash
git clone https://github.com/appelflap/domoticz-millheat.git millheat
```

Alternatively you can download the latest version from
https://github.com/appelflap/domoticz-millheat/archive/master.zip
and unzip it. Then create a directory on your Domoticz device
in `domoticz/plugins` named `millheat` and transfer all the
files to your device.

Restart your Domoticz service with:

```bash
sudo service domoticz.sh restart
```

Now go to **Setup**, **Hardware** in your Domoticz interface. There you add
**MillHeat**.

Make sure you enter all the required fields for authentication.
