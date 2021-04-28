#!/usr/bin/python3

import EntranceMusic

device_mac_addresses_to_mp3 = {
  "C4:98:80:E0:8F:01": ""
}

autopair = EntranceMusic.EntranceMusic(device_mac_addresses_to_mp3)

autopair.enable_pairing()