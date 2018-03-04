from subprocess import check_output

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