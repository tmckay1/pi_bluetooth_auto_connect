# pi_bluetooth_auto_connect
Automatically connect your raspberry pi to a bluetooth device when the device is near

### Allow the Phone to Pair to the Raspberry Pi

https://www.raspberrypi.org/forums/viewtopic.php?p=947185#p947185

You'll need to add the SP profile to the Pi. Edit this file:

```
sudo nano /etc/systemd/system/dbus-org.bluez.service
```

Add the compatibility flag, ' -C', at the end of the 'ExecStart=' line. Add a new line after that to add the SP profile. The two lines should look like this:

```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

Save the file and reboot. Pair and trust your Pi and phone with bluetoothctl.

Now, in a terminal on the Pi, enter the following:

```
sudo rfcomm watch hci0
```

Now you can connect from the app and send text or macros. You can read it on the Pi with minicom, or in Python with PySerial or whatever serial comm software you prefer.

-------------

### How to Initiate Pair

Command line does not work for some reason. So you need to have already paired in the UI with the device before. To do this make the pi discoverable in the menu bar in the UI, on the phone tap to connect, then accept the connection in the raspberry pi. Once this happens you can disconnect and running the auto connect script will work.

------------

### Copy over files

Make bluezutils accessible from the system packages

```
sudo cp bluezutils.py /usr/local/lib/python3.7/dist-packages/
```

Copy over the agent to the system bin and change the perms to make it executable

```
sudo cp auto-agent.py /usr/local/bin/auto-agent
sudo chmod 744 /usr/local/bin/auto-agent
```

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
