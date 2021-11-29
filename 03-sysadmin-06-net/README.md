# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. Работа c HTTP через телнет.
   - Подключитесь утилитой телнет к сайту stackoverflow.com
   `telnet stackoverflow.com 80`
- отправьте HTTP запрос
    ```bash
    GET /questions HTTP/1.0
    HOST: stackoverflow.com
    [press enter]
    [press enter]
    ```
- В ответе укажите полученный HTTP код, что он 

    ```bash
    vagrant@vagrant:~$ telnet stackoverflow.com 80
    Trying 151.101.1.69...
    Connected to stackoverflow.com.
    Escape character is '^]'.
    GET /questions HTTP/1.0
    HOST: stackoverflow.com
    
    HTTP/1.1 301 Moved Permanently
    cache-control: no-cache, no-store, must-revalidate
    location: https://stackoverflow.com/questions
    x-request-guid: 0094b144-ca9c-4b46-9fba-9926a1036730
    feature-policy: microphone 'none'; speaker 'none'
    content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
    Accept-Ranges: bytes
    Date: Mon, 29 Nov 2021 15:45:05 GMT
    Via: 1.1 varnish
    Connection: close
    X-Served-By: cache-fra19153-FRA
    X-Cache: MISS
    X-Cache-Hits: 0
    X-Timer: S1638200705.188882,VS0,VE93
    Vary: Fastly-SSL
    X-DNS-Prefetch-Control: off
    Set-Cookie: prov=b5b11993-2616-c332-36db-86d5f6e26741; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly
    
    Connection closed by foreign host.```
    
Вместо **_http_** сервер ожидает **_https_** запрос.

2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers`
- укажите в ответе полученный HTTP код.
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
- приложите скриншот консоли браузера в ответ.
[Скриншот](https://yadi.sk/i/8bru7B9fJTw54g)
3. Какой IP адрес у вас в интернете?
[Адрес](https://yadi.sk/i/G4zaZK8cuUyFfw)
4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois`

    ```bash
   % Information related to '5.228.0.0/16AS42610'

    route:          5.228.0.0/16
    descr:          NCNET
    origin:         AS42610
    mnt-by:         NCNET-MNT
    mnt-lower:      NCNET-MNT
    created:        2012-09-07T12:16:12Z
    last-modified:  2012-09-07T12:16:12Z
    source:         RIPE
    ```
5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`

    ```bash
    vagrant@vagrant:~$ traceroute -IAn 8.8.8.8
    traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
     1  10.0.2.2 [*]  0.390 ms  0.252 ms  0.355 ms
     2  192.168.17.171 [*]  7.313 ms  8.089 ms  8.942 ms
     3  192.168.0.1 [*]  50.441 ms  51.189 ms  51.168 ms
     4  * * *
     5  77.37.250.210 [AS42610]  12.960 ms  13.717 ms  14.408 ms
     6  72.14.209.81 [AS15169]  14.387 ms  22.146 ms  22.112 ms
     7  209.85.250.231 [AS15169]  22.095 ms  10.612 ms  10.979 ms
     8  108.170.250.113 [AS15169]  18.506 ms  19.125 ms *
     9  * * *
    10  74.125.253.94 [AS15169]  32.932 ms  33.576 ms  33.559 ms
    11  216.239.58.53 [AS15169]  30.596 ms  31.278 ms  25.427 ms
    12  * * *
    13  * * *
    14  * * *
    15  * * *
    16  * * *
    17  * * *
    18  * * *
    19  * * *
    20  * * *
    21  * 8.8.8.8 [AS15169]  23.629 ms  25.123 ms
    ```
6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?

    ```bash
                                                                    My traceroute  [v0.93]
    vagrant (10.0.2.15)                                                                                                          2021-11-29T16:16:44+0000
    Keys:  Help   Display mode   Restart statistics   Order of fields   quit
                                                                                                                 Packets               Pings
     Host                                                                                                      Loss%   Snt   Last   Avg  Best  Wrst StDev
     1. AS???    10.0.2.2                                                                                       0.0%    19    0.3   0.5   0.3   1.2   0.2
     2. AS???    192.168.17.171                                                                                 0.0%    19    5.1   5.6   4.2   8.9   1.1
     3. AS???    192.168.0.1                                                                                    0.0%    19   11.4   9.4   7.8  12.8   1.5
     4. (waiting for reply)
     5. AS42610  77.37.250.210                                                                                 61.1%    18   10.7  10.7   8.8  11.9   1.2
     6. AS15169  72.14.209.81                                                                                   0.0%    18    9.8  17.4   8.9  44.3   9.4
     7. AS15169  209.85.250.231                                                                                 0.0%    18    9.5  10.6   9.3  13.3   1.1
     8. AS15169  108.170.250.113                                                                               22.2%    18    9.8  14.6   8.9  28.4   6.5
     9. AS15169  142.251.49.158                                                                                76.5%    18   24.1  23.4  22.3  24.1   0.8
    10. AS15169  74.125.253.94                                                                                  0.0%    18   22.7  27.6  22.5  44.1   6.0
    11. AS15169  216.239.58.53                                                                                  0.0%    18   28.7  28.5  25.6  32.9   2.3
    12. (waiting for reply)
    13. (waiting for reply)
    14. (waiting for reply)
    15. (waiting for reply)
    16. (waiting for reply)
    17. (waiting for reply)
    18. (waiting for reply)
    19. (waiting for reply)
    20. (waiting for reply)
    21. AS15169  8.8.8.8                                                                                       44.4%    18   26.1  26.0  24.3  27.7   1.1
   ```
7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`

    ```bash
    vagrant@vagrant:~$ dig +trace @8.8.8.8 dns.google NS
    dns.google.             10800   IN      NS      ns2.zdns.google.
    dns.google.             10800   IN      NS      ns3.zdns.google.
    dns.google.             10800   IN      NS      ns1.zdns.google.
    dns.google.             10800   IN      NS      ns4.zdns.google.
    dns.google.             900     IN      A       8.8.8.8
    dns.google.             900     IN      A       8.8.4.4
    ```
8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`

    ```bash
    vagrant@vagrant:~$ dig -x 8.8.8.8
    
    ; <<>> DiG 9.16.1-Ubuntu <<>> -x 8.8.8.8
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15760
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
    
    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 65494
    ;; QUESTION SECTION:
    ;8.8.8.8.in-addr.arpa.          IN      PTR
    
    ;; ANSWER SECTION:
    8.8.8.8.in-addr.arpa.   8348    IN      PTR     dns.google.
    ```

В качестве ответов на вопросы можно приложите лог выполнения команд в консоли или скриншот полученных результатов.
