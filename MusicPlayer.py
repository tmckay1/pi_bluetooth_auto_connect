"""Class to encapsulate a player object to play music"""
class MusicPlayer:

  # A dict of MAC Addresses pointing to an MP3 to play when we connect to the address
  device_mac_addresses_to_mp3 = {}

  def __init__(self, device_mac_addresses_to_mp3):
    self.device_mac_addresses_to_mp3 = device_mac_addresses_to_mp3

  def play(self, mac_address):
    print("Playing music for: " + self.device_mac_addresses_to_mp3[mac_address])
