from subprocess import check_output
from datetime   import datetime

# ---

class Network:

  def __init__ (self, BSSID, SSID, network_type, authentication, encryption, protocol, channel):

    self.BSSID          = BSSID
    self.SSID           = SSID
    self.network_type   = network_type
    self.authentication = authentication
    self.encryption     = encryption
    self.protocol       = protocol
    self.last_seen      = datetime.now()
    self.channel        = channel

    # ---

  def update_signal_strength (self, signal_strength):

    self.signal_strength = signal_strength
    self.last_seen       = datetime.now()

# ---

def display_connection_status ():

  print()
  connection_status = get_connection_status()
  if connection_status['State'] == 'connected':
    print('Connected to ' + connection_status['SSID'] + ' (' + connection_status['BSSID'] + ')')
  else:
    print('Disconnected.')

# ---

def get_connection_status ():

  result = {}
  output = str(check_output('netsh wlan show interface wi-fi'))

  for line in output.split('\\r\\n'):
    pair = line.split(' : ')
    if len(pair) == 2:
      result[pair[0].strip()] = pair[1].strip()

  return result

# ---

def get_network_list ():

  networks = {}

  # Get all nearby networks using netsh
  netsh_output = str(check_output('netsh wlan show networks mode=bssid'))

  # For each SSID
  for result in netsh_output.split('\\r\\nSSID')[1:]:

    # Split the result into key/value pairs
    pairs = result.split('\\r\\n')
    SSID = pairs[0].split(' : ')[1].strip()
    network_type = pairs[1].split(' : ')[1].strip()
    authentication = pairs[2].split(' : ')[1].strip()
    encryption = pairs[3].split(' : ')[1].strip()

    # For each BSSID
    for sub_result in result.split('BSSID')[1:]:

      # Split the result into key/value pairs
      sub_pairs = sub_result.split('\\r\\n')
      BSSID = sub_pairs[0].split(' : ')[1].strip()
      signal = sub_pairs[1].split(' : ')[1].strip()
      protocol = sub_pairs[2].split(' : ')[1].strip()
      channel = sub_pairs[3].split(' : ')[1].strip()

      # Record the network details
      networks[BSSID] = Network(BSSID, SSID, network_type, authentication, encryption, protocol, channel)
      networks[BSSID].update_signal_strength(signal)

  return networks