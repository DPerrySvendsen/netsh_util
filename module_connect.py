from subprocess      import check_output
from datetime        import datetime
from time            import sleep
from utils           import NL, confirm, try_call
from module_profiles import get_profile_list, \
                            generate_profile, \
                            add_profile, \
                            delete_profile

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

# ---

def autocomplete_network (SSID):

  for network in get_network_list().values():
    if network.SSID.lower().startswith(SSID.lower()):
      return network

# ---

def connect_to_network (name):

  print()

  # Are we already connected?
  connection_status = get_connection_status()
  if connection_status['State'] == 'connected':
    print('Already connected to ' + connection_status['SSID'] + ' (' + connection_status['BSSID'] + ')')
    if confirm('Disconnect?'):
      disconnect_from_network()
      print()
    else:
      return

  # Is there a nearby network with this SSID?
  target_network = autocomplete_network(name)

  if not target_network:
    print('Could not locate ' + name)
    return

  print('Found network ' + target_network.SSID + ' (' + target_network.BSSID + ')')
  print('Security: ' + target_network.authentication + ' (' + target_network.encryption + ')' + NL)

  # Does a profile exist for this SSID?
  for profile_SSID, profile_name in get_profile_list().items():
    if profile_SSID.lower() == target_network.SSID.lower():

      if confirm('Use existing profile?'):
        # Attempt to connect using the existing profile
        print()
        attempt_connection(profile_name)
        return

      else:
        print(NL + 'This will overwrite the existing profile.')
        if confirm('Are you sure?'):
          # Delete the existing profile
          delete_profile(profile_name)
          print()
        else:
          return

  # Generate a new profile
  profile = generate_profile(target_network)

  # Add the network password, if required
  if target_network.authentication not in ['None', 'Open']:
    password = input('Password required: ')
    profile = profile.format(password)

  # Attempt to connect using the new profile
  command_result = add_profile(profile)
  if not command_result['Success']:
    print(command_result['Output'])
    return

  attempt_connection(target_network.SSID)

  # ---

def attempt_connection (profile_name):

  print('Sending connection request...')
  command_result = try_call(['netsh', 'wlan', 'connect', profile_name])

  if not command_result['Success']:
    print(command_result['Output'])

  try:
    # Check if the request was successful
    for i in range(5):
      sleep(1)
      if get_connection_status()['State'] == 'connected':
        print('Connected.')
        return

  except KeyboardInterrupt:
    pass

  print('Request timed out.' + NL)
  print('This may mean the network is no longer available or the network password is incorrect')
  if confirm('Delete associated profile?'):
    delete_profile(profile_name)

# ---

def disconnect_from_network ():

  print()

  connection_status = get_connection_status()
  if connection_status['State'] == 'disconnected':
    print('Not connected to a network.')
    return

  command_result = try_call('netsh wlan disconnect')

  if command_result['Success']:
    print('Disconnected from ' + connection_status['SSID'])
  else:
    print('Disconnect failed.')
    print(command_result['Output'])