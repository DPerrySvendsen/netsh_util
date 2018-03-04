from argparse       import ArgumentParser
from module_connect import display_connection_status
from module_scanner import WifiScanner

parser = ArgumentParser(
  prog        = 'netsh_util',
  description = 'Network Shell Utility: Used to manage wireless network connections.'
)

group = parser.add_mutually_exclusive_group()
group.add_argument('-s', '--status',       action  = 'store_true', help = 'show the current wi-fi connection status')
group.add_argument('-S', '--scan',         action  = 'store_true', help = 'scan for wireless networks')
group.add_argument('-c', '--connect',      metavar = 'SSID',       help = 'connect to a wireless network with the specified SSID')
group.add_argument('-d', '--disconnect',   action  = 'store_true', help = 'disconnect from the current wireless network')
group.add_argument('-l', '--listprofiles', action  = 'store_true', help = 'list all stored profiles')
group.add_argument('-p', '--profile',      metavar = 'name',       help = 'display the contents of the specified profile')
group.add_argument('-D', '--delete',       action  = 'store_true', help = 'delete a stored profile')

args = vars(parser.parse_args())

if args['status']:
  display_connection_status()
  pass

elif args['scan']:
  WifiScanner().run()
  pass

elif args['connect']:
  pass

elif args['disconnect']:
  pass

elif args['listprofiles']:
  pass

elif args['profile']:
  pass

elif args['delete']:
  pass