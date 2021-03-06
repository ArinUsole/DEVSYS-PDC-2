# Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`.

   `chdir("/tmp")                           = 0` _chdir, fchdir - change working directory_
2. Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:
    ```bash
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
    ```
    Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.

   `openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3`
3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

   ```bash
   vagrant@vagrant:~$ ping ya.ru > png.txt &
   [1] 5048
   vagrant@vagrant:~$ rm png.txt
   vagrant@vagrant:~$ sudo lsof -p 5048 | grep png.txt
   ping    5048 vagrant    1w   REG  253,0     3261 131087 /home/vagrant/png.txt (deleted)
   vagrant@vagrant:~$ sudo sh
   # echo > /proc/5048/fd/1
   # exit
   vagrant@vagrant:~$ sudo lsof -p 5048 | grep png.txt
   ping    5048 vagrant    1w   REG  253,0    39418 131087 /home/vagrant/png.txt (deleted)
   vagrant@vagrant:~$ sudo cat /proc/5048/fd/1 | wc -l
   159
   vagrant@vagrant:~$ sudo cat /proc/5048/fd/1 | wc -l
   162
   ```
4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

   _Зомби не занимают памяти (как процессы-сироты), но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом._
5. В iovisor BCC есть утилита `opensnoop`:
    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    ```
    На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).

   ```bash
   openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libselinux.so.1", O_RDONLY|O_CLOEXEC) = 3
   openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
   openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpcre2-8.so.0", O_RDONLY|O_CLOEXEC) = 3
   openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
   openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
   ```
6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.

   _uname - get name and information about current kernel.
   Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}_
7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
   ```bash
   root@netology1:~# test -d /tmp/some_dir; echo Hi
   Hi
   root@netology1:~# test -d /tmp/some_dir && echo Hi
   root@netology1:~#
   ```
   Есть ли смысл использовать в bash `&&`, если применить `set -e`?

   ```bash
   A list is a sequence of one or more pipelines separated by one of the operators ;, &, &&, or ||, and optionally terminated by one of ;,  &,
      or <newline>.
   ...
   command1 && command2
   command2 is executed if, and only if, command1 returns an exit status of zero (success).
   ...
   set -e  Exit immediately if a command exits with a non-zero status.
   ``` 
   таким образом, использования `set -e` ни как не влияет на использование `&&`   
8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?

   ```bash
   -e  Exit immediately if a command exits with a non-zero status.
   -u  Treat unset variables as an error when substituting.
   -x  Print commands and their arguments as they are executed.
   -o option-name
        pipefail     the return value of a pipeline is the status of
                     the last command to exit with a non-zero status,
                     or zero if no command exited with a non-zero status
   ```
   _удобная отладка сценариев_.
9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

   ```bash
   D    uninterruptible sleep (usually IO)
   I    Idle kernel thread
   R    running or runnable (on run queue)
   S    interruptible sleep (waiting for an event to complete)
   T    stopped by job control signal
   t    stopped by debugger during the tracing
   W    paging (not valid since the 2.6.xx kernel)
   X    dead (should never be seen)
   Z    defunct ("zombie") process, terminated but not reaped by its parent
   ```
   
   ```bash
   vagrant@vagrant:~$ ps ax o stat | sort | uniq -c
     11 I
     44 I<
      1 R+
     33 S
      4 S+
      1 Sl
      1 SLsl
      2 SN
      1 S<s
     16 Ss
      2 Ss+
      5 Ssl
      1 STAT
   ```
   `S interruptible sleep (waiting for an event to complete)` наиболее часто встречающийся статус у процессов в системе
