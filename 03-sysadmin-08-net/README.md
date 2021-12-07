# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```

```bash
route-views>show ip route 5.228.205.37
Routing entry for 5.228.0.0/16
  Known via "bgp 6447", distance 20, metric 0
  Tag 3356, type external
  Last update from 4.68.4.46 2w6d ago
  Routing Descriptor Blocks:
  * 4.68.4.46, from 4.68.4.46, 2w6d ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 3356
      MPLS label: none
```
2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.

```bash
172.16.10.0/24 dev dummy0 scope link
172.16.100.0/24 dev dummy0 scope link metric 100
172.16.200.0 dev dummy0 scope link metric 10
```
3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.

```bash
root@vagrant:/home/vagrant# ss -a -r -t -4
State           Recv-Q          Send-Q                   Local Address:Port                              Peer Address:Port           Process
LISTEN          0               4096                      localhost%lo:domain                                 0.0.0.0:*
LISTEN          0               128                            0.0.0.0:ssh                                    0.0.0.0:*
LISTEN          0               4096                           0.0.0.0:rpc.portmapper                         0.0.0.0:*
ESTAB           0               0                              vagrant:ssh                                   _gateway:63228
```
4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?

```bash
root@vagrant:/home/vagrant# ss -a -r -u -4
State           Recv-Q          Send-Q                   Local Address:Port                               Peer Address:Port          Process
UNCONN          0               0                              0.0.0.0:rpc.portmapper                          0.0.0.0:*
UNCONN          0               0                            localhost:snmp                                    0.0.0.0:*
UNCONN          0               0                         localhost%lo:domain                                  0.0.0.0:*
UNCONN          0               0                         vagrant%eth0:bootpc                                  0.0.0.0:*
```
5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали. 

[Диаграмма](https://yadi.sk/i/e5w1G_9I940jRA)
