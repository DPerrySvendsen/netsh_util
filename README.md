# netsh_util

Network Shell Utility (netsh_util) is a Python tool intended to make it easier to manage wireless network connections from the Windows command line. It can be used to scan for and connect to nearby networks, as well as view and manage saved profiles.

```
usage: netsh_util [-h] [-s | -S | -c SSID | -d | -l | -p name | -D name]

Network Shell Utility: Used to manage wireless network connections.

optional arguments:
  -h, --help            show this help message and exit
  -s, --status          show the current wi-fi connection status
  -S, --scan            scan for wireless networks
  -c SSID, --connect SSID
                        connect to a wireless network with the specified SSID
  -d, --disconnect      disconnect from the current wireless network
  -l, --listprofiles    list all stored profiles
  -p name, --profile name
                        display the contents of the specified profile
  -D name, --delete name
                        delete a stored profile
```
