import subprocess
import optparse
import re
from pip._vendor.distlib.compat import raw_input


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its mac address for")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="new mac address for the interface")
    (options, argumnets) = parser.parse_args()
    if not options.interface:
        parser.error("enter a name for the interface ")
    elif not options.new_mac_address:
        parser.error("enter a new mac addresss ")
    return options


def mac_changer(interface, new_mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_check = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_check:
        return mac_check.group(0)
    else:
        print("[-] Could not change the mac address ")


options = get_arguments()

mac_changer(options.interface, options.new_mac_address)
if get_mac(options.interface) == options.new_mac_address:
    print("[+] The mac address has been changed successfully to " + get_mac(options.interface))
else:
    print("[-] The mac address is " + str(get_mac(options.interface)))
