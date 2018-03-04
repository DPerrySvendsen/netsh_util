from subprocess import call
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