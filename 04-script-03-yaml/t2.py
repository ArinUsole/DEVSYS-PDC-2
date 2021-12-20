import socket
import time
import json
import yaml


def write_hosts(dt: dict):
    with open('hosts.json', 'w') as js:
        js.write(json.dumps(dt))
    with open('hosts.yaml', 'w') as ya:
        ya.write(yaml.dump(dt))


hosts = {'drive.google.com': '', 'mail.google.com': '', 'google.com': ''}
while True:
    for host in hosts:
        ip = socket.gethostbyname(host)
        if not hosts[host]:
            print(f'<{host}> - <{ip}>')
            hosts[host] = ip
            write_hosts(hosts)
        elif ip != hosts[host] and hosts[host]:
            print(f'[ERROR] <{host}> IP mismatch: <{hosts[host]}> <{ip}>')
            hosts[host] = ip
            write_hosts(hosts)
    time.sleep(5)
