#!/usr/bin/python3
# encoding=utf8

import sys
import time
import pexpect
import subprocess

class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass

"""Class to auto pair and trust with bluetooth."""
class EntranceMusic:
  # Whether or not we are connected to a device
  device_is_not_connected = True

  # The list of MAC Addresses to try to connect to
  device_mac_addresses = []

  # A dict of MAC Addresses pointing to an MP3 to play when we connect to the address
  device_mac_addresses_to_mp3 = {}

  # The message to look for when we successfully connect to a device
  DEVICE_CONNECT_SUCCESS_MESSAGE = "dev_connect successful"

  def __init__(self, device_mac_addresses_to_mp3):
    out = subprocess.check_output("/usr/sbin/rfkill unblock bluetooth", shell = True)
    self.child = pexpect.spawn("bluetoothctl", echo = False)
    self.device_mac_addresses_to_mp3 = device_mac_addresses_to_mp3
    for mac_address in self.device_mac_addresses_to_mp3:
      self.device_mac_addresses.append(mac_address)

  def get_output(self,command, response = "succeeded"):
    """Run a command in bluetoothctl prompt, return output as a list of lines."""
    self.child.send(command + "\n")
    pause = 0
    time.sleep(pause)
    start_failed = self.child.expect([response, pexpect.EOF])

    if start_failed:
        raise BluetoothctlError("Bluetoothctl failed after running " + command)
        
    return self.child.before.split(b"\r\n")

  def enable_pairing(self):
    """Make device visible to scanning and enable pairing."""
    print("pairing enabled")
    try:
      out = self.get_output("power on")
      out = self.get_output("discoverable on")
      out = self.get_output("pairable on")
      out = self.get_output("agent off", "unregistered")
      self.try_to_connect()

    except BluetoothctlError as e:
      print("Error running commands for bluetoothctl in enable_pairing")
      print(e)
      return None

  def disable_pairing(self):
    """Disable devices visibility and ability to pair."""
    try:
      out = self.get_output("discoverable off")
      out = self.get_output("pairable off")

    except BluetoothctlError as e:
      print("Error running commands for bluetoothctl in disable_pairing")
      print(e)
      return None

  def try_to_connect(self):
    while self.device_is_not_connected:
      for mac_address in self.device_mac_addresses:
        try:
          with subprocess.Popen(["/usr/local/bin/auto-agent",mac_address], shell = False, stdout = subprocess.PIPE) as p:
            out, errors = p.communicate()
            out = out.decode("utf-8")
            print("Outout from /usr/local/bin/auto-agent for device: " + mac_address)
            print(out)
            if self.DEVICE_CONNECT_SUCCESS_MESSAGE in out:
              print("Connection to " + mac_address + " successful")
              self.device_is_not_connected = False
            else:
              print("Connection to " + mac_address + " failed")

        except Exception as e:
          print("Error in connecting device: " + mac_address)
          print(e)