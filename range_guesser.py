"""
Useful when:
* You got some big subnets  - i.e. 10.232.0.0/16 - to cut into smaller ones
* You have no information regarding which ranges are used within the network
your are auditing.

Generate the list of every first and last host's IP address of any
private range possible based on a specific netmask (/24 by default).

You can then use this list for scanning and assume the range is used if a host was found.
As simple as that :)

Private IPv4 addresses:

      CIDR      |         IP address range          |    Number of addresses
----------------|-----------------------------------|-------------------------
10.0.0.0/8      |   10.0.0.0 – 10.255.255.255       |   2**(32-8) = 16 777 216
172.16.0.0/12   |   172.16.0.0 – 172.31.255.255     |   2**(32-12) = 1 048 576
192.168.0.0/16  |   192.168.0.0 – 192.168.255.255   |   2**(32-16) = 65 536
"""

import sys
import shlex
import argparse
from subprocess import run, PIPE
from ipaddress import IPv4Network

def usage():
    """Argument parser function."""
    parser = argparse.ArgumentParser(description='Hosts list generator to smartly identify subnets within your scope')
    parser.add_argument('-o', '--output', default='hosts.lst')
    parser.add_argument('-s', '--subnet', help="If you get some big subnet - i.e. 10.232.0.0/16 - to cut into smaller ones", default=None)
    parser.add_argument('-n', '--netmask', type=int, default=24)
    parser.add_argument('--scan', help="Perform scanning after host list generation", action="store_true")
    parser.add_argument('-c', '--command', help="Specify your nmap command - i.e. nmap -oA subnets_guess -iL hosts.lst --top-ports=10", default='nmap -sn -oA subnets_guess -iL hosts.lst')
    return parser.parse_args()

def gen_list(filename='hosts.lst', sub=24, subnet=None):
    """Host list generator function."""
    ip_list = []
    if subnet:
        subnet_list = list(IPv4Network(subnet).subnets(new_prefix=sub))
    else:
        a_class = list(IPv4Network('10.0.0.0/8').subnets(new_prefix=sub))
        b_class = list(IPv4Network('172.16.0.0/12').subnets(new_prefix=sub))
        c_class = list(IPv4Network('192.168.0.0/16').subnets(new_prefix=sub))
        subnet_list = a_class + b_class + c_class

    for cpt, subnet in enumerate(subnet_list):
        # First host (removing network address)
        ip_list.append(subnet[1])
        # Last host (removing broadcast address)
        ip_list.append(subnet[-2])

    with open(filename, 'w') as fd_out:
        fd_out.write('\n'.join([str(host) for host in ip_list]))

def scan(nmap_command):
    """Nmap scanner launcher."""
    res = run(shlex.split(nmap_command), stdout=PIPE, stderr=PIPE)
    if not res.returncode:
        sys.stdout.write(res.stdout.decode('utf-8'))
    else:
        sys.stdout.write(res.stderr.decode('utf-8'))

if __name__ == '__main__':
    args = usage()
    gen_list(args.output, args.netmask, args.subnet)
    if args.scan:
        scan(args.command)
