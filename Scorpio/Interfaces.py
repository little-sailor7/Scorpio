from collections import namedtuple
import re
import subprocess

def get_interfaces(external=True, ip=False):

    name_pattern = "^(\w+)\s"
    mac_pattern = ".*?HWaddr[ ]([0-9A-Fa-f:]{17})" if external else ""
    ip_pattern = ".*?\n\s+inet[ ]addr:((?:\d+\.){3}\d+)" if ip else ""
    pattern = re.compile("".join((name_pattern, mac_pattern, ip_pattern)),
                            flags=re.MULTILINE)

    ifconfig = subprocess.check_output("ifconfig").decode()
    interfaces = pattern.findall(ifconfig)
    if external or ip:
        Interface = namedtuple("Interface", "name {mac} {ip}".format(
            mac="mac" if external else "",
            ip="ip" if ip else ""))
        return [Interface(*interface) for interface in interfaces]
    else:
        return interfaces


if __name__ == "__main__":
    interfaces = get_interfaces(external=True)
    for interface in interfaces:
        print("{name}: {ip}".format(name=interface.name, ip=interface.ip))