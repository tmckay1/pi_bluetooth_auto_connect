import dbus
import dbus.service

class Agent(dbus.service.Object):
  exit_on_release = True
  mainloop = None

  def set_exit_on_release(self, exit_on_release):
    self.exit_on_release = exit_on_release

  def set_mainloop(self, mainloop):
    self.mainloop = mainloop

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="", out_signature="")
  def Release(self):
    print("Release")
    if self.exit_on_release:
      self.mainloop.quit()

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="os", out_signature="")
  def AuthorizeService(self, device, uuid):
    print("AuthorizeService (%s, %s)" % (device, uuid))
    return # automatically authorize connection
    authorize = ask("Authorize connection (yes/no): ")
    if (authorize == "yes"):
      return
    raise Rejected("Connection rejected by user")

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="o", out_signature="s")
  def RequestPinCode(self, device):
    print("RequestPinCode (%s)" % (device))
    set_trusted(device)
    #return ask("Enter PIN Code: ")
    return "0000" # return default PIN Code of 0000

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="o", out_signature="u")
  def RequestPasskey(self, device):
    print("RequestPasskey (%s)" % (device))
    set_trusted(device)
    #passkey = ask("Enter passkey: ")
    passkey = "0000" # return default passkey of 0000
    return dbus.UInt32(passkey)

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="ouq", out_signature="")
  def DisplayPasskey(self, device, passkey, entered):
    print("DisplayPasskey (%s, %06u entered %u)" %
            (device, passkey, entered))

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="os", out_signature="")
  def DisplayPinCode(self, device, pincode):
    print("DisplayPinCode (%s, %s)" % (device, pincode))

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="ou", out_signature="")
  def RequestConfirmation(self, device, passkey):
    print("RequestConfirmation (%s, %06d)" % (device, passkey))
    set_trusted(device)
    return # automatically trust
    confirm = ask("Confirm passkey (yes/no): ")
    if (confirm == "yes"):
      set_trusted(device)
      return
    raise Rejected("Passkey doesn't match")

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="o", out_signature="")
  def RequestAuthorization(self, device):
    print("RequestAuthorization (%s)" % (device))
    return # automatically authorize
    auth = ask("Authorize? (yes/no): ")
    if (auth == "yes"):
      return
    raise Rejected("Pairing rejected")

  @dbus.service.method(AGENT_INTERFACE,
          in_signature="", out_signature="")
  def Cancel(self):
    print("Cancel")