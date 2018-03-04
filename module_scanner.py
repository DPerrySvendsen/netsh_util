from module_connect import get_network_list
from utils          import NL, ConsoleColour, cls, get_key_pressed
from datetime       import datetime, timedelta
from msvcrt         import kbhit
from math           import floor

class WifiScanner:

  networks = {}
  refresh_rate = 10
  timeout_rate = 30

  # ---

  def update_network_list(self):
    # Refresh the list of nearby networks
    for BSSID, network in get_network_list().items():
      self.networks[BSSID] = network

  # ---

  def format_network_string(self, network):

    BSSID = network.BSSID
    SSID  = network.SSID

    # Clamp the SSID
    if len(SSID) > 25:
      SSID = SSID[:22] + '...'
    SSID = SSID.ljust(25)

    # Pad the remaining values
    authentication = network.authentication.ljust(18)
    encryption     = network.encryption    .ljust(10)
    protocol       = network.protocol      .ljust(10)
    channel        = network.channel       .rjust(6)

    # WPA was officially replaced by WPA2 in 2006
    if network.authentication[:4] == 'WPA-':
      authentication = ConsoleColour.YELLOW + authentication + ConsoleColour.END

    if network.encryption == 'None':
      encryption = '          '
    # WEP is considered completely insecure, and is deprecated as of 802.11i (2004)
    elif network.encryption == 'WEP':
      encryption = ConsoleColour.RED    + encryption + ConsoleColour.END
    # TKIP is no longer considered secure, and is deprecated as of 802.11mb (2012)
    elif network.encryption == 'TKIP':
      encryption = ConsoleColour.YELLOW + encryption + ConsoleColour.END

    # We highlight networks using anything other than 802.11n, just because it's a bit unusual
    if network.protocol != '802.11n':
      protocol = ConsoleColour.YELLOW + protocol + ConsoleColour.END

    # Very rarely, we come across an 'ah-hoc' network
    adhoc = network.network_type != 'Infrastructure'
    if adhoc:
      BSSID = ConsoleColour.PURPLE + BSSID + ConsoleColour.END

    # How long has it been since the network was last seen?
    time_since_seen = floor((datetime.now() - network.last_seen).total_seconds())

    signal_strength = ''

    if time_since_seen > self.timeout_rate:
      # For timed-out networks, display last seen time
      signal_strength = network.last_seen.strftime('%I:%M%p')

    elif time_since_seen > self.refresh_rate:
      # For inactive networks, display seconds since last seen
      signal_strength = '{}s ago'.format(str(time_since_seen)).rjust(7)

    else:
      # For active connections, display signal strength
      signal_strength = network.signal_strength.rjust(7)
      if not adhoc:
        BSSID = ConsoleColour.GREEN + BSSID + ConsoleColour.END
      SSID  = ConsoleColour.GREEN + SSID + ConsoleColour.END

    # Build the entry
    return ' ' + BSSID + ' ' + SSID + ' ' + authentication + ' ' + encryption + ' ' + protocol + ' ' + channel + ' ' + signal_strength

  # ---

  def print_network_list(self):

    # Print table header
    table = ' BSSID             SSID                      Authentication     Encryption Protocol  Channel Signal ' + \
       NL + ' ---               ---                       ---                ---        ---       ---     ---    '

    # Sort the network list
    sorted_network_list = sorted(
      self.networks.values(),
      key = lambda network: (
        # Show active networks at the top, timed out networks at the bottom
        (datetime.now() - network.last_seen).total_seconds() > self.refresh_rate,
        # By signal strength (descending)
        int(network.signal_strength[:-1]) * -1,
        # By SSID
        network.SSID
      ),
    )

    for network in sorted_network_list:
      table += NL + self.format_network_string(network)

    # Clear console and print all at once
    cls()
    print(NL + table)
    print(NL + '[Esc] Exit')

  # ---

  def run (self):

    last_update = datetime.now() - timedelta(seconds = self.refresh_rate)

    try:
      while True:
        if kbhit() and get_key_pressed() == 'Escape':
          break
        if datetime.now() > last_update + timedelta(seconds = self.refresh_rate):
          last_update = datetime.now()
          self.update_network_list()
          self.print_network_list()

    except KeyboardInterrupt:
      pass