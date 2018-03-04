from subprocess import call, check_output, CalledProcessError
from msvcrt     import getch

# ---

NL = '\n'
CONTROL_CHAR = b'\xe0'

# ---

class ConsoleColour:

  RED        = '\033[91m'
  GREEN      = '\033[92m'
  YELLOW     = '\033[93m'
  LIGHT_BLUE = '\033[94m'
  PURPLE     = '\033[95m'
  DARK_BLUE  = '\033[96m'
  END        = '\033[0m'

# ---

def cls ():

  call('cls', shell = True)

# ---

def try_call (command):

  result = {
    'Success' : True,
    'Output'  : ''
  }

  try:
    result['Output'] = check_output(command)
  except CalledProcessError as ex:
    result['Success'] = False
    result['Output']  = str(ex.output).replace('\\r', '').replace('\\n', '')[2:-1]

  return result

# ---

def confirm (message):

  input_value = ''
  while input_value not in ['Y', 'N']:
    input_value = input(message + ' [Y/N]: ').upper().strip()
  return input_value == 'Y'

# ---

def get_key_pressed ():

  control_characters = {
    b'H'    : 'Up',
    b'P'    : 'Down',
    b'K'    : 'Left',
    b'M'    : 'Right',
    b'\r'   : 'Enter',
    b'\x1b' : 'Escape'
  }

  code = getch()
  if code == CONTROL_CHAR:
    code = getch()
  if code in control_characters:
    return control_characters[code]
  else:
    return code.decode('utf-8')