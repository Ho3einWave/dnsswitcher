import os
import re
import ctypes
import sys


version = "V1.0.2"

stream = os.popen("netsh interface ipv4 show config")
output = stream.read()
interfaces = output.split("\n\n")

ctypes.windll.kernel32.SetConsoleTitleW(f"DNS Switcher {version}")

interface_regex = "Configuration\sfor\sinterface\s\"(.*)\"\n\s*DHCP\senabled:\s*(.*)\n\s*IP\sAddress\:\s*(\d{1,255}.\d{1,255}.\d{1,255}.\d{1,255})\n\s*Subnet\sPrefix\:\s*(\d{1,255}.\d{1,255}.\d{1,255}.\d{1,255}\/\d{1,25}).*\n\s*Default\sGateway\:\s*(\d{1,255}.\d{1,255}.\d{1,255}.\d{1,255})\n"

dns_obj = {
    "electro": ["78.157.42.100", "78.157.42.101"],
    "radar": ["10.202.10.10", "10.202.10.11"],
    "shecan": ["185.51.200.2", "178.22.122.100"],
    "google": ["8.8.8.8", "4.2.2.4"],
    "cloudflare": ["1.1.1.1", "1.0.0.1"],
    "yandex": ["77.88.8.8", "77.88.8.1"]
}

networks = []


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():

    for iface in interfaces:
        re_result = re.findall(interface_regex, iface)
        if len(re_result) > 0:
            interface_info = re_result[0]
            network = {
                "name": interface_info[0],
                "dhcp": interface_info[1],
                "ip": interface_info[2],
                "subnet": interface_info[3],
                "gateway": interface_info[4]
            }
            networks.append(network)

    for idx, net in enumerate(networks):
        name = net["name"]
        ip = net["ip"]
        subnet = net["subnet"]
        gateway = net["gateway"]
        dhcp = net["dhcp"]

        print(
            f"{idx+1}.\n  Network: {name}\n  IP: {ip}\n  Subnet: {subnet}\n  Gateway: {gateway}\n  DHCP: {dhcp}\n")

    network_index = int(input("Which Network You Want To Set DNS? "))
    selected_network = networks[network_index - 1]["name"]

    print('''
    Game:
        1. Electro    - 2. Radar

    Other:
        3. Shecan     - 4. Google
        5. CloudFlare - 6. Yandex

        0. Clear DNS
    ''')
    index_of_dns = ["electro", "radar", "shecan",
                    "google", "cloudflare", "yandex"]
    dns_index = int(input("Which DNS You Want To Apply? "))

    if dns_index == 0:
        stream = os.popen(
            f"netsh interface ip set dns name=\"{selected_network}\" source=dhcp")
    else:
        selected_dns = dns_obj[index_of_dns[dns_index-1]]

        stream = os.popen(
            f"netsh interface ip set dns name=\"{selected_network}\" source=dhcp")

        stream = os.popen(
            f"netsh interface ip set dns name=\"{selected_network}\" static {selected_dns[0]}")

        stream = os.popen(
            f"netsh interface ip add dns name=\"{selected_network}\" {selected_dns[1]} index=2")

    input("\nSuccess! Press Any Key To Exit.")
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
