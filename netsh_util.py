from argparse        import ArgumentParser
from module_scanner  import WifiScanner
from module_connect  import display_connection_status, \
                            connect_to_network, \
                            disconnect_from_network
from module_profiles import list_all_profiles, \
                            display_profile, \
                            delete_profile

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
group.add_argument('-D', '--delete',       metavar = 'name',       help = 'delete a stored profile')

args = vars(parser.parse_args())

if args['status']:
  display_connection_status()

elif args['scan']:
  WifiScanner().run()

elif args['connect']:
  connect_to_network(args['connect'])

elif args['disconnect']:
  disconnect_from_network()

elif args['listprofiles']:
  list_all_profiles()

elif args['profile']:
  display_profile(args['profile'])

elif args['delete']:
  delete_profile(args['delete'])

else:
  parser.print_help()