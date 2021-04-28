#!/usr/bin/python3

import EntranceMusic
import MusicPlayer

# A dict of MAC Addresses pointing to an MP3 to play when we connect to the address
device_mac_addresses_to_mp3 = {
  "C4:98:80:E0:8F:01": "/home/pi/test.mp3"
}

# The list of MAC Addresses to try to connect to
device_mac_addresses = []

# Fill in list of mac addresses from dict
for mac_address in device_mac_addresses_to_mp3:
  device_mac_addresses.append(mac_address)

music_player = MusicPlayer.MusicPlayer(device_mac_addresses_to_mp3)
autopair = EntranceMusic.EntranceMusic(device_mac_addresses, music_player)

autopair.enable_pairing()