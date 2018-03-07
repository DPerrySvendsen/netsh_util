from subprocess import check_output
from utils      import NL, try_call
from os         import remove
from utils      import confirm

# ---

def list_all_profiles ():
  print()
  for name in get_profile_list().values():
    print(' ' + name)

# ---

def display_profile (name):

  profile = autocomplete_profile(name)

  if not profile:
    print('Profile not found.')
    return

  print()
  for key, value in profile.items():
    print(' ' + key + ': ' + value)

# ---

def delete_profile (name):

  profile = autocomplete_profile(name)

  if not profile:
    print('Profile not found.')
    return

  if confirm('Delete profile ' + profile['Name'] + '?'):
    try_call(['netsh', 'wlan', 'delete', 'profile', profile['Name']])
    print('Profile deleted.')

# ---

def get_profile_list ():

  # Returns a mapping of SSID to profile name
  # Assumes each SSID is associated with only one profile

  result = {}
  netsh_output = str(check_output('netsh wlan show profiles *'))

  for profile in netsh_output.split('Profile information')[1:]:
    name = ''
    SSID = ''
    for line in profile.split('\\r\\n'):
      pair = line.split(' : ')
      if len(pair) == 2:
        key = pair[0].strip()
        value = pair[1].strip().replace('"', '')
        if key == 'SSID name':
          SSID = value
        elif key == 'Name':
          name = value
    result[SSID] = name

  return result

# ---

def autocomplete_profile (profile_name):
  for name in get_profile_list().values():
    if name.lower().startswith(profile_name.lower()):
      return get_profile_details(name)

# ---

def profile_exists (profile_name):

  return try_call(['netsh', 'wlan', 'show', 'profile', profile_name])['Success']

# ---

def get_profile_details (profile_name):

  result = {}
  netsh_output = str(check_output(['netsh', 'wlan', 'show', 'profile', profile_name]))

  for line in netsh_output.split('\\r\\n'):
    pair = line.split(' : ')
    if len(pair) == 2:
      key = pair[0].strip()
      value = pair[1].strip()
      if key not in result:
        result[key] = value

  return result

# ---

def generate_profile (network):

  # TODO: This doesn't yet handle all network configurations. Need to test.

  if network.network_type != 'Infrastructure':
    return None

  authentication = 'open'
  encryption = 'none'

  authentication_protocol = network.authentication.split('-')
  if len(authentication_protocol) == 2:
    if authentication_protocol[0] == 'WPA':
      authentication = 'WPA'
      # TODO: Personal/Enterprise?
    elif authentication_protocol[0] == 'WPA2':
      if authentication_protocol[1] == 'Enterprise':
        authentication = 'WPA2'
      elif authentication_protocol[1] == 'Personal':
        authentication = 'WPA2PSK'
  else:
    if network.authentication != 'Open':
      print('Authentication string unrecognised: ' + network.authentication)
      return None

  if network.authentication[:3] == 'WPA':

    if network.authentication[3] == '2':
      authentication = 'WPA2PSK'
    else:
      authentication = 'WPAPSK'

    if network.encryption == 'TKIP':
      encryption = 'TKIP'
    elif network.encryption == 'CCMP':
      encryption = 'AES'

  elif network.encryption == 'WEP':
    encryption = 'WEP'

  profile_schema = '<?xml version="1.0"?>' + NL + \
                   ' <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1"> ' + NL + \
                   '   <name>{}</name>                                                         ' + NL + \
                   '   <SSIDConfig>                                                            ' + NL + \
                   '     <SSID>                                                                ' + NL + \
                   '       <name>{}</name>                                                     ' + NL + \
                   '     </SSID>                                                               ' + NL + \
                   '   </SSIDConfig>                                                           ' + NL + \
                   '   <connectionType>ESS</connectionType>                                    ' + NL + \
                   '   <MSM>                                                                   ' + NL + \
                   '     <security>                                                            ' + NL + \
                   '       <authEncryption>                                                    ' + NL + \
                   '         <authentication>{}</authentication>                               ' + NL + \
                   '         <encryption>{}</encryption>                                       ' + NL + \
                   '       </authEncryption>                                                   ' + NL + \
                   ('     <sharedKey>                                                          ' + NL +
                    '       <keyType>passPhrase</keyType>                                      ' + NL +
                    '       <protected>false</protected>                                       ' + NL +
                    '       <keyMaterial>{}</keyMaterial>                                      ' + NL +
                    '     </sharedKey>                                                         ' + NL
                      if authentication != 'open' else '') + \
                   '     </security>                                                           ' + NL + \
                   '   </MSM>                                                                  ' + NL + \
                   ' </WLANProfile>                                                            '

  return profile_schema.format(network.SSID, network.SSID, authentication, encryption, '{}')

# ---

def add_profile (profile):

  # Save the XML in a temp file, import the profile, then delete the temp file
  file = open('profile.xml', 'w')
  file.write(profile)
  file.close()
  result = try_call('netsh wlan add profile profile.xml')
  remove('profile.xml')
  del (file)
  return result