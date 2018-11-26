# domoticz-millheat
Domoticz MillHeat Plugin

Work in progress! Not yet tested.

Short summary
-------------

Add virtual devices for your MillHeat devices to your [Domoticz](https://www.domoticz.com/)

Get full device status from the API into your Domoticz
Current info:
* asdfasdf
* asdfasdf2

Installation and setup
----------------------

If you are use a Raspberry Pi to host your Domoticz, you probably need to install libpython3.4 for plugins to work.

```bash
sudo apt install python3-dev python3-pip
pip3 install --upgrade pip
pip3 install millheater
# or sometimes:
python3 -m pip install millheater
```

In your `domoticz/plugins` directory do

```bash
cd domoticz/plugins
git clone https://github.com/appelflap/domoticz-millheat.git
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

Make sure you enter all the required fields.
