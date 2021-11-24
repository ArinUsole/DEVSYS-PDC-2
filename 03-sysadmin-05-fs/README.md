# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

    _**Разрежённый файл** (англ. sparse file) — файл, в котором последовательности нулевых байтов[1] заменены на информацию об этих последовательностях (список дыр)._

2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

    _Файлы, являющиеся жесткой ссылкой на один объект, имеют общий inode (первичный идентификатор объекта на файловой системе или индексный дескриптор).
    Индексные дескрипторы хранят информацию о файлах, такую как принадлежность владельцу (пользователю и группе), режим доступа (чтение, запись, запуск на выполнение) и тип файла._

3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

    `sudo sfdisk -d /dev/sdb | sfdisk /dev/sdc`

6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

    `sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1`

7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.

    `sudo mdadm --create --verbose /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2`

8. Создайте 2 независимых PV на получившихся md-устройствах.

    `sudo pvcreate /dev/md0 /dev/md1`

9. Создайте общую volume-group на этих двух PV.

    `sudo lvcreate all_md /dev/md0 /dev/md1`

10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

    `sudo lvcreate -L 100 -n testlv all_md /dev/md1`

11. Создайте `mkfs.ext4` ФС на получившемся LV.

    `sudo mkfs.ext4 /dev/all_md/testlv`

12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

    ```bash
    mkdir -p /tmp/new
    sudo mount /dev/all_md/testlv /tmp/new
    ```

13. Поместите туда тестовый файл, например 
 
    `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

14. Прикрепите вывод `lsblk`.

    ```bash
    vagrant@vagrant:~$ lsblk
    NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                    8:0    0   64G  0 disk
    ├─sda1                 8:1    0  512M  0 part  /boot/efi
    ├─sda2                 8:2    0    1K  0 part
    └─sda5                 8:5    0 63.5G  0 part
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
    sdb                    8:16   0  2.5G  0 disk
    ├─sdb1                 8:17   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    └─sdb2                 8:18   0  511M  0 part
      └─md1                9:1    0 1017M  0 raid0
        └─all_md-testlv  253:2    0  100M  0 lvm   /tmp/new
    sdc                    8:32   0  2.5G  0 disk
    ├─sdc1                 8:33   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    └─sdc2                 8:34   0  511M  0 part
      └─md1                9:1    0 1017M  0 raid0
        └─all_md-testlv  253:2    0  100M  0 lvm   /tmp/new
    ```

15. Протестируйте целостность файла:

     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# echo $?
     0
     ```

16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

    ```bash
    root@vagrant:/home/vagrant# lsblk
    NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                    8:0    0   64G  0 disk
    ├─sda1                 8:1    0  512M  0 part  /boot/efi
    ├─sda2                 8:2    0    1K  0 part
    └─sda5                 8:5    0 63.5G  0 part
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
    sdb                    8:16   0  2.5G  0 disk
    ├─sdb1                 8:17   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    │   └─all_md-testlv  253:2    0  100M  0 lvm   /tmp/new
    └─sdb2                 8:18   0  511M  0 part
      └─md1                9:1    0 1017M  0 raid0
    sdc                    8:32   0  2.5G  0 disk
    ├─sdc1                 8:33   0    2G  0 part
    │ └─md0                9:0    0    2G  0 raid1
    │   └─all_md-testlv  253:2    0  100M  0 lvm   /tmp/new
    └─sdc2                 8:34   0  511M  0 part
      └─md1                9:1    0 1017M  0 raid0
    ```

17. Сделайте `--fail` на устройство в вашем RAID1 md.

    `root@vagrant:/home/vagrant# mdadm --fail /dev/md0 /dev/sdc1`

18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

    ```bash
    [18082.998088] md/raid1:md0: Disk failure on sdc1, disabling device.
                   md/raid1:md0: Operation continuing on 1 devices.
    ```
19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# echo $?
     0
     ```
    
    ```bash
    root@vagrant:/home/vagrant# gzip -t /tmp/new/test.gz && echo $?
    0
    ```

20. Погасите тестовый хост, `vagrant destroy`.

