### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```json
    {
      "info": "Sample JSON output from our service\t",
      "elements": [
        {
          "name": "first",
          "type": "server",
          "ip": "7175"
        },
        {
          "name": "second",
          "type": "proxy",
          "ip": "71.78.22.43"
        }
      ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
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

```

### Вывод скрипта при запуске при тестировании:
```bash
<drive.google.com> - <108.177.15.194>
<mail.google.com> - <64.233.163.17>
<google.com> - <216.239.38.120>
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"drive.google.com": "108.177.15.194", "mail.google.com": "64.233.163.17", "google.com": "216.239.38.120"}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
drive.google.com: 108.177.15.194
google.com: 216.239.38.120
mail.google.com: 64.233.163.17
```
