# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | TypeError: unsupported operand type(s) for +: 'int' and 'str'  |
| Как получить для переменной `c` значение 12?  | c = str(a) + b  |
| Как получить для переменной `c` значение 3?  | c = a + int(b)  |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

bash_command = ["cd ~", "git status"]
if (sys.platform == 'win32'):
    cmd = 'cd'
elif (sys.platform == 'linux'):
    cmd = 'pwd'
path = os.popen(f'{bash_command[0]} && {cmd}').read().replace('\n', '')

result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(f'{path}/{prepare_result}')
```

### Вывод скрипта при запуске при тестировании:
```
vagrant@vagrant:~$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   t1.sh
        modified:   t2.sh
        modified:   t3.sh

no changes added to commit (use "git add" and/or "git commit -a")
vagrant@vagrant:~$ ./t1.sh
/home/vagrant/t1.sh
/home/vagrant/t2.sh
/home/vagrant/t3.sh
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

if (len(sys.argv) == 1):
        cd = "."
else:
        cd = sys.argv[1]
bash_command = [f"cd {cd}", "git status"]
if (sys.platform == 'win32'):
    cmd = 'cd'
elif (sys.platform == 'linux'):
    cmd = 'pwd'
path = os.popen(f'{bash_command[0]} && {cmd}').read().replace('\n', '')

result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(f'{path}/{prepare_result}')
```

### Вывод скрипта при запуске при тестировании:
```
vagrant@vagrant:~$ ./t1.sh
/home/vagrant/t1.sh
/home/vagrant/t2.sh
/home/vagrant/t3.sh
vagrant@vagrant:~$ ./t1.sh ~
/home/vagrant/t1.sh
/home/vagrant/t2.sh
/home/vagrant/t3.sh
vagrant@vagrant:~$ ./t1.sh /etc/
fatal: not a git repository (or any of the parent directories): .git
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import socket
import time

hosts = {'drive.google.com':'', 'mail.google.com':'', 'google.com':''}
while (True):
    for host in hosts:
        ip = socket.gethostbyname(host)
        if (not hosts[host]):
            print(f'<{host}> - <{ip}>')
            hosts[host] = ip
        elif (ip != hosts[host] and hosts[host]):
            print(f'[ERROR] <{host}> IP mismatch: <{hosts[host]}> <{ip}>')
            hosts[host] = ip
    time.sleep(5)
```

### Вывод скрипта при запуске при тестировании:
```bash
vagrant@vagrant:~$ ./t1.sh
<drive.google.com> - <142.250.150.194>
<mail.google.com> - <142.250.186.165>
<google.com> - <216.239.38.120>
[ERROR] <mail.google.com> IP mismatch: <142.250.186.165> <173.194.73.83>
[ERROR] <mail.google.com> IP mismatch: <173.194.73.83> <173.194.73.17>
[ERROR] <google.com> IP mismatch: <216.239.38.120> <64.233.162.102>
```
