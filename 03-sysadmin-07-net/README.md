# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

```buildoutcfg
ipconfig /all #windows
ip -br l #linux
ifconfig #RHEL
```
2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

```buildoutcfg
LLDP – протокол для обмена информацией между соседними устройствами, позволяет определить к какому порту коммутатора подключен сервер.
```
```bash
apt install lldpd
systemctl enable lldpd && systemctl start lldpd

DESCRIPTION
     lldpd is a daemon able to receive and send LLDP frames. The Link Layer Discovery Protocol is a vendor-neutral Layer 2 protocol that allows a
     network device to advertise its identity and capabilities on the local network.
```
3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.

```buildoutcfg
VLAN – виртуальное разделение коммутатора
```
```bash
DESCRIPTION
       The  vlan action allows to perform 802.1Q en- or decapsulation on a packet, reflected by the operation modes POP, PUSH and MODIFY.  The POP
       mode is simple, as no further information is required to just drop the outer-most VLAN encapsulation. The PUSH and MODIFY modes require  at
       least a VLANID and allow to optionally choose the VLANPROTO to use.
       
vi /etc/network/interfaces

auto vlan100
iface vlan100 inet static
  address 192.168.1.1
  netmask 255.255.255.0
  vlan_raw_device eth0
auto eth0.100
iface eth0.100 inet static
  address 192.168.1.1
  netmask 255.255.255.0
  vlan_raw_device eth0
```
4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

```buildoutcfg
LAG – агрегация портов
mode = 0 (round robin) 
Круговой, циклически использует физические интерфейсы для передачи пакетов. Рекомендован для включения «по умолчанию». Этот режим работает с максимальной отдачей

mode = 1 (active-backup)
Работает только один интерфейс, остальные находятся в очереди горячей замены. Если ведущий интерфейс перестает функционировать, то его нагрузку подхватывает следующий (присвоив mac-адрес) и становится активным. Дополнительная настройка коммутатора не требуется.

mode = 2 (balance-xor)
XOR политика: Передача на основе [(исходный MAC-адрес → XOR → MAC-адрес получателя) %число интерфейсов]. Эта команда выбирает для каждого получателя определенный интерфейс в соответствии с mac-адресом. Режим обеспечивает балансировку нагрузки и отказоустойчивость.

mode = 3 (broadcast)
Все пакеты передаются на все интерфейсы в группе. Режим обеспечивает отказоустойчивость.

mode = 4 (802.3ad)
IEEE 802.3ad Dynamic Link aggregation (динамическое объединение каналов). Создает агрегации групп, имеющие одни и те же скорости и дуплексные настройки. Использует все включенные интерфейсы в активном агрегаторе согласно спецификации 802.3ad.
Предварительные реквизиты
Поддержка ethtool (позволяет отображать или изменять настройки сетевой карты) базы драйверов для получения скорости и дуплекса каждого интерфейса.
Коммутатор с поддержкой IEEE 802.3ad Dynamic Link aggregation. Большинство параметров потребует некоторой конфигурации для режима 802.3ad.

mode =5 (balance-tlb)
Адаптивная балансировка передаваемой нагрузки: канал связи не требует какой либо специальной настройки. Исходящий трафик распределяется в соответствии с текущей нагрузкой (вычисляется по скоростям) для каждого интерфейса. Входящий трафик принимается текущим интерфейсом. Если принимающий интерфейс выходит из строя, то следующий занимает его место приватизировав его mac-адрес.
Поддержка ethtool (позволяет отображать или изменять настройки сетевой карты) базы драйверов для получения скорости и дуплекса каждого интерфейса.

mode = 6 (balance-alb)
Адаптивное перераспределение нагрузки: включает balance-tlb плюс receive load balancing (rlb) для трафика IPv4 и не требует специального конфигурирования. То есть все так же как и при mode =5, только и входящий трафик балансируется между интерфейсами. Полученная балансировка нагрузки достигается опросом ARP. Драйвер перехватывает ответы ARP, направленные в локальной системе в поисках выхода и перезаписывает исходный адрес сетевой карты с уникальным аппаратным адресом одного из интерфейсов в группе.
```
```bash
vi /etc/modules

bonding mode=0 miimon=100

modprobe bonding mode=0 miimon=100

vi /etc/network/interfaces

# The bond0 network interface
auto bond0
allow-hotplug bond0
iface bond0 inet static
address <ip-address>
netmask <netmask>
network <network-address>
broadcast <broadcast-address>
gateway <gateway-address>
dns-nameservers <nameserver-one> <nameserver-two>
dns-search <domain-name>
up /sbin/ifenslave bond0 eth0
up /sbin/ifenslave bond0 eth1

/etc/init.d/networking restart
```
5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.

```buildoutcfg
Сколько IP адресов в сети с маской /29. Всего 8, узловых 6.
Сколько /29 подсетей можно получить из сети с маской /24. 256/8=32 подсети.
Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
vagrant@vagrant:~$ ipcalc 10.10.10.0/29
Address:   10.10.10.0           00001010.00001010.00001010.00000 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
HostMin:   10.10.10.1           00001010.00001010.00001010.00000 001
HostMax:   10.10.10.6           00001010.00001010.00001010.00000 110
Broadcast: 10.10.10.7           00001010.00001010.00001010.00000 111
Hosts/Net: 6                     Class A, Private Internet

vagrant@vagrant:~$ ipcalc 10.10.10.8/29
Address:   10.10.10.8           00001010.00001010.00001010.00001 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.8/29        00001010.00001010.00001010.00001 000
HostMin:   10.10.10.9           00001010.00001010.00001010.00001 001
HostMax:   10.10.10.14          00001010.00001010.00001010.00001 110
Broadcast: 10.10.10.15          00001010.00001010.00001010.00001 111
Hosts/Net: 6                     Class A, Private Internet

vagrant@vagrant:~$ ipcalc 10.10.10.16/29
Address:   10.10.10.16          00001010.00001010.00001010.00010 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.16/29       00001010.00001010.00001010.00010 000
HostMin:   10.10.10.17          00001010.00001010.00001010.00010 001
HostMax:   10.10.10.22          00001010.00001010.00001010.00010 110
Broadcast: 10.10.10.23          00001010.00001010.00001010.00010 111
Hosts/Net: 6                     Class A, Private Internet 
```
6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

```buildoutcfg
192.0.2.0/24	Для примеров в документации.
```
7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?

```bash
vagrant@vagrant:~$ arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.0.2.3                 ether   52:54:00:12:35:03   C                     eth0
10.0.2.2                 ether   52:54:00:12:35:02   C                     eth0

Clearing cache with arp command
The arp utility does not accept an option to clear the full cache. Instead, it allows to flush out entries found with the -d option.
sudo arp -d 10.0.2.3
vagrant@vagrant:~$ arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.0.2.2                 ether   52:54:00:12:35:02   C                     eth0

The ip tool has a more advanced way to clear out the full ARP cache.
sudo ip -s -s neigh flush all
10.0.2.2 dev eth0 lladdr 52:54:00:12:35:02 ref 1 used 23/0/18 probes 1 REACHABLE

*** Round 1, deleting 1 entries ***
*** Flush is complete after 1 round ***
```
