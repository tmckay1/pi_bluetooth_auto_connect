# pi_bluetooth_auto_connect
Automatically connect your raspberry pi to a bluetooth device when the device is near and play entrance music based on the device's mac address. This library was used from an example library given in forums. Links to that are further below. The basic architecture/design of this program is you will have a system executable `auto-agent` which you can use as a background job if you would like. That executable will try to connect to a given mac address. Based on it's success/failure it will output different messages to `stdout`.

The main file of this library is `EntranceMusic.py` which creates a child process to call `auto-agent` for a list of mac addresses. If we are able to successfully connect to a mac address, then play a music file that is associated with that mac address. Otherwise, go down the list again and try to connect with bluetooth. The assumption is when the person's phone is close enough to connect to the pi, entrance music will start playing for that device.

It may seem a bit odd to have a file that can act as a job (`auto-agent`) instead of creating an object/class to encapsulate that logic, but I chose to keep it this way since this will give you an idea of what else you can do with bluetooth commands in python. We are only using a targeted part of this functionality, but if you are interested in building more complex applications, then this will give you and idea of what else you can do.

### Allow the Phone to Pair to the Raspberry Pi

Resource: https://www.raspberrypi.org/forums/viewtopic.php?p=947185#p947185

You first need to enable your phone to connect to the pi. I was not able to do this by default, so you'll need to add the SP profile to the Pi. Edit this file:

```
sudo nano /etc/systemd/system/dbus-org.bluez.service
```

Add the compatibility flag, ' -C', at the end of the 'ExecStart=' line. Add a new line after that to add the SP profile. The two lines should look like this:

```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

Save the file and reboot.

-------------

### How to Initiate Pair

After you enable your phone to pair (I have an iPhone 10), you need to initiate the pair in the UI and connect the Pi to the phone. Command line does not work for some reason. So you need to have already paired in the UI with the device before. To do this make the pi discoverable in the menu bar in the pi desktop UI, on the phone tap to connect, then accept the connection in the raspberry pi. Once this happens you can disconnect and running the auto connect script will work.

------------

### Download Repo and Copy over files

First download the repo with:

```
git clone https://github.com/tmckay1/pi_bluetooth_auto_connect.git
```

Next make bluezutils accessible from the system packages (you'll need to do this since we use auto-agent to call bluezutils and auto-agent is later copied to a system directory)

```
sudo cp bluezutils.py /usr/local/lib/python3.7/dist-packages/
```

Copy over the agent to the system bin and change the perms to make it executable

```
sudo cp auto-agent.py /usr/local/bin/auto-agent
sudo chmod 744 /usr/local/bin/auto-agent
```

This is only so you can run the auto-agent in the background in a job if you wanted. You can abstract out the implementation into a regular python class if you would like.

-------------

### Run the Test File

Now that you ran the above commands you should be able to run the test file. First you'll need to edit `testAutoPair.py` file which contains a dict of mac addresses pointing to music files to play for each device when connected to that device. Make sure to use the mac addresses of your devices. To find them you can open the command line in the raspberry pi and run `bluetoothctl`. Then run `scan on` when you enter the bluetoothctl shell. Wait for you device to show up (make sure it's discoverable) and you'll see the mac address. After editing the file, run

```
sudo python3 ./testAutoPair.py
```

within the directory of the git folder.

-------------

### Automatically Connecting to Bluetooth

https://raspberrypi.stackexchange.com/questions/53408/automatically-connect-trusted-bluetooth-speaker

https://www.raspberrypi.org/forums/viewtopic.php?t=170353

-------------

### Example Logs

```
2021-04-06 23:53:00,343 - bt_auto_loader - INFO - Starting to monitor Bluetooth connections
2021-04-06 23:53:31,992 - bt_auto_loader - INFO - Getting dbus interface for device: /org/bluez/hci0/dev_C4_98_80_E0_8F_01 interface: org.freedesktop.DBus.Properties property_name: org.bluez.MediaControl1
2021-04-06 23:53:31,993 - bt_auto_loader - INFO - Device: C4_98_80_E0_8F_01 has disconnected
2021-04-06 23:53:42,650 - bt_auto_loader - INFO - Getting dbus interface for device: /org/bluez/hci0/dev_C4_98_80_E0_8F_01 interface: org.freedesktop.DBus.Properties property_name: org.bluez.MediaControl1
2021-04-06 23:53:42,651 - bt_auto_loader - INFO - Device: C4_98_80_E0_8F_01 has disconnected
2021-04-06 23:59:29,715 - bt_auto_loader - INFO - Shutting down
2021-04-07 00:00:54,612 - bt_auto_loader - INFO - Starting to monitor Bluetooth connections
2021-04-07 00:01:51,449 - bt_auto_loader - INFO - Getting dbus interface for device: /org/bluez/hci0/dev_C4_98_80_E0_8F_01 interface: org.freedesktop.DBus.Properties property_name: org.bluez.MediaControl1
2021-04-07 00:01:51,450 - bt_auto_loader - INFO - Device: C4_98_80_E0_8F_01 has disconnected
2021-04-07 00:02:03,476 - bt_auto_loader - INFO - Getting dbus interface for device: /org/bluez/hci0/dev_C4_98_80_E0_8F_01 interface: org.freedesktop.DBus.Properties property_name: org.bluez.MediaControl1
2021-04-07 00:02:03,477 - bt_auto_loader - INFO - Running cmd: pactl load-module module-loopback source=bluez_source.C4_98_80_E0_8F_01
```
