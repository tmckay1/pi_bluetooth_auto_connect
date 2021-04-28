import pygame

"""Class to encapsulate a player object to play music"""
class MusicPlayer:

  # A dict of MAC Addresses pointing to an MP3 to play when we connect to the address
  device_mac_addresses_to_mp3 = {}

  def __init__(self, device_mac_addresses_to_mp3):
    self.device_mac_addresses_to_mp3 = device_mac_addresses_to_mp3

  def play(self, mac_address):
    audio_file_path = self.device_mac_addresses_to_mp3[mac_address]
    print("Playing music for: " + audio_file_path)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

