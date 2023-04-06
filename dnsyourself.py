#!/usr/bin/env python3

### setup system
import argparse

### required, what dns should I be?
### optional, what IP should redirect the dns to? usually my own, will attempt to generate automatically...
parser = argparse.ArgumentParser()
parser.add_argument('domain', help='What domain name should I serve?')
parser.add_argument('-ip', '--ip', help='What IP should I direct the domain to?')
args = parser.parse_args()

### get check inputs.. what is my IP?
ip = args.ip
domain = args.domain

### if no ip source ip
if None == ip:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

print("Serving Domain: '{}' as: '{}'".format(domain, ip))

### generate dns file
dns = """{domain}.              IN  SOA    dns.{domain}. {domain}. 1675303881 7200 3600 1209600 3600
dns.{domain}.          IN  A      {ip}
{domain}.          IN  A      {ip}
""".format(domain=domain, ip=ip)

dnsFile = open('domain.to.serve', 'w', newline='')
dnsFile.write(dns)
dnsFile.close()
print("Created dns file 'domain.to.serve'")

### generate coredns file
core = """
.:53 {
    forward . 8.8.8.8 1.1.1.1
    errors
    health
}

{domain}.:53 {
    log
    errors
    health
    file domain.to.serve
}
""".format(domain=domain)

dnsFile = open('Corefile', 'w', newline='')
dnsFile.write(dns)
dnsFile.close()
print("Created Corefile")

### prompt user to run the script
print("Run: `./coredns run`")
print("If you have errors you may require sudo, or to `systemctl stop systemd-resolved.service`")