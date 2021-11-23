# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

   * поместите его в автозагрузку,
   * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
   * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

   ```bash
   sudo useradd --system --shell /bin/false node_exporter
   wget https://github.com/prometheus/node_exporter/releases/download/v1.3.0/node_exporter-1.3.0.linux-amd64.tar.gz
   tar xvfz node_exporter-1.3.0.linux-amd64.tar.gz
   sudo cp node_exporter-1.3.0.linux-amd64/node_exporter /usr/local/bin
   sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
   ```
   ```bash
   sudo tee /etc/systemd/system/node_exporter.service <<"EOF"
   [Unit]
   Description=Node Exporter
   
   [Service]
   User=node_exporter
   Group=node_exporter
   EnvironmentFile=-/etc/sysconfig/node_exporter
   ExecStart=/usr/local/bin/node_exporter $OPTIONS
   
   [Install]
   WantedBy=multi-user.target
   EOF
   ```
   ```bash
   sudo systemctl daemon-reload && sudo systemctl start node_exporter && sudo systemctl status node_exporter && sudo systemctl enable node_exporter
   ```
   ```bash
   vagrant@vagrant:~$ systemctl status node_exporter
   ● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2021-11-23 05:30:34 UTC; 1h 2min ago
   Main PID: 628 (node_exporter)
      Tasks: 6 (limit: 2278)
     Memory: 18.4M
     CGroup: /system.slice/node_exporter.service
             └─628 /usr/local/bin/node_exporter
   ```
   ```bash
   vagrant@vagrant:~$ sudo !!
   sudo systemctl stop node_exporter.service
   vagrant@vagrant:~$ systemctl status node_exporter
   ● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Tue 2021-11-23 06:35:07 UTC; 9s ago
    Process: 628 ExecStart=/usr/local/bin/node_exporter $OPTIONS (code=killed, signal=TERM)
   Main PID: 628 (code=killed, signal=TERM)
   ```
   ```bash
   vagrant@vagrant:~$ sudo systemctl start node_exporter.service
   vagrant@vagrant:~$ systemctl status node_exporter
   ● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2021-11-23 06:36:56 UTC; 7s ago
   Main PID: 1347 (node_exporter)
      Tasks: 5 (limit: 2278)
     Memory: 2.7M
     CGroup: /system.slice/node_exporter.service
             └─1347 /usr/local/bin/node_exporter
   ```

2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

   ```bash
   # TYPE node_cpu_seconds_total
   
   # TYPE node_memory_*
   
   # TYPE node_disk_io_time_seconds_total
   
   # TYPE node_network_receive_bytes_total
   ```
      
3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    ```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
    ```

    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

   ```bash
   Detailed information for each CPU of the system.
   Detailed information about the memory management of the system.
   Charts with performance information for all the system disks.
   Metrics for the networking stack of the system.
   Resources utilization of systemd services.
   Per application statistics are collected using netdata's apps.plugin.
   ```

4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

   Думаю, что понимает:
   ```bash
   vagrant@vagrant:~$ dmesg | grep box
   [    1.695216] vboxvideo: loading out-of-tree module taints kernel.
   [    1.695248] vboxvideo: module verification failed: signature and/or required key missing - tainting kernel
   [    1.696212] vboxvideo: loading version 6.1.24 r145751
   [    1.707368] fbcon: vboxvideodrmfb (fb0) is primary device
   [    1.711210] vboxvideo 0000:00:02.0: fb0: vboxvideodrmfb frame buffer device
   [    1.836342] [drm] Initialized vboxvideo 1.0.0 20130823 for 0000:00:02.0 on minor 0
   [    4.360921] vboxguest: Successfully loaded version 6.1.24 r145751
   [    4.361046] vboxguest: misc device minor 58, IRQ 20, I/O port d020, MMIO at 00000000f0400000 (size 0x400000)
   [    4.361048] vboxguest: Successfully loaded version 6.1.24 r145751 (interface 0x00010004)
   [    8.304608] vboxsf: g_fHostFeatures=0x8000000f g_fSfFeatures=0x1 g_uSfLastFunction=29
   [    8.304667] *** VALIDATE vboxsf ***
   [    8.304677] vboxsf: Successfully loaded version 6.1.24 r145751
   [    8.304725] vboxsf: Successfully loaded version 6.1.24 r145751 on 5.4.0-80-generic SMP mod_unload modversions  (LINUX_VERSION_CODE=0x5047c)
   [    8.305805] vboxsf: SHFL_FN_MAP_FOLDER failed for '/vagrant': share not found
   ```
   
5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?

   ```bash
   vagrant@vagrant:~$ sysctl fs.nr_open
   fs.nr_open = 1048576
   ```
   ```bash
   vagrant@vagrant:~$ ulimit -n
   1024
   ```
   
6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.

   ```bash
   vagrant@vagrant:~$ sudo su
   root@vagrant:/home/vagrant# unshare -f --pid --mount-proc sleep 1h
   ^Z
   [1]+  Stopped                 unshare -f --pid --mount-proc sleep 1h
   root@vagrant:/home/vagrant# lsns
        NS TYPE   NPROCS   PID USER            COMMAND
   ...
   4026531836 pid       123     1 root            /sbin/init
   ...
   4026532186 pid         1  1577 root            sleep 1h
   ...
   root@vagrant:/home/vagrant# nsenter --target 1577 --pid --mount
   root@vagrant:/# ps aux
   USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
   root           1  0.0  0.0   8076   588 pts/0    S    08:19   0:00 sleep 1h
   root           2  0.0  0.1   9836  3836 pts/0    S    08:36   0:00 -bash
   root          11  0.0  0.1  11492  3252 pts/0    R+   08:36   0:00 ps aux
   ```
   
7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

   Рекурсивная бомба, другими словами код можно представить как:
   ```bash
   bomb() { 
   bomb | bomb &
   }; bomb
   ```
   Ограничивается через shell resource limits:
   ```bash
   vagrant@vagrant:~$ ulimit -a
   ...
   max user processes              (-u) 7595
   ```
