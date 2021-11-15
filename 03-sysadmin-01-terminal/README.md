# Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"

1. Установите средство виртуализации [Oracle VirtualBox](https://www.virtualbox.org/).
**YES**
2. Установите средство автоматизации [Hashicorp Vagrant](https://www.vagrantup.com/).
**YES**
3. В вашем основном окружении подготовьте удобный для дальнейшей работы терминал. Можно предложить:
* Windows Terminal в Windows
**YES**
4. С помощью базового файла конфигурации запустите Ubuntu 20.04 в VirtualBox посредством Vagrant:
```bash
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'bento/ubuntu-20.04' version '202107.28.0' is up to date...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => C:/DEVSYS-PDC-2/03-sysadmin-01-terminal
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
```
5. Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?
**YES**
6. Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: [документация](https://www.vagrantup.com/docs/providers/virtualbox/configuration.html). Как добавить оперативной памяти или ресурсов процессора виртуальной машине?
```bash
config.vm.provider "virtualbox" do |vb|
	vb.cpus = "4"
	vb.memory = "2048"
end
```
7. Команда `vagrant ssh` из директории, в которой содержится Vagrantfile, позволит вам оказаться внутри виртуальной машины без каких-либо дополнительных настроек. Попрактикуйтесь в выполнении обсуждаемых команд в терминале Ubuntu.
```bash
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 15 Nov 2021 06:39:55 AM UTC

  System load:  0.0               Processes:             139
  Usage of /:   2.5% of 61.31GB   Users logged in:       0
  Memory usage: 7%                IPv4 address for eth0: 10.0.2.15
  Swap usage:   0%


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Thu Nov 11 08:54:56 2021 from 10.0.2.2
```
8. Ознакомиться с разделами `man bash`, почитать о настройках самого bash:
* какой переменной можно задать длину журнала `history`, и на какой строчке manual это описывается?
```bash
HISTSIZE
	The number of commands to remember in the command history (see HISTORY below).  If the value is 0, commands are  not  saved  in  the
	history list.  Numeric values less than zero result in every command being saved on the history list (there is no limit).  The shell
	sets the default value to 500 after reading any startup files.
```
* что делает директива `ignoreboth` в bash?
```bash
Bash also interprets a number of multi-character options.  These options must appear on the command line before  the  single-character  op‐
...skipping...
	previous history entry to not be saved.  A value of ignoreboth is shorthand for ignorespace and ignoredups.  A  value  of  erasedups
	causes all previous lines matching the current line to be removed from the history list before that line is saved.  Any value not in
	the above list is ignored.  If HISTCONTROL is unset, or does not include a valid value, all lines read by the shell parser are saved
	on  the  history list, subject to the value of HISTIGNORE.  The second and subsequent lines of a multi-line compound command are not
	tested, and are added to the history regardless of the value of HISTCONTROL.
```
9. В каких сценариях использования применимы скобки `{}` и на какой строчке `man bash` это описано?
_Manual page bash(1) line 232/3993 6% (press h for help or q to quit)_
```bash
{ list; }
    list  is simply executed in the current shell environment.  list must be terminated with a newline or semicolon.  This is known as a
    group command.  The return status is the exit status of list.  Note that unlike the metacharacters ( and ), {  and  }  are  reserved
    words  and must occur where a reserved word is permitted to be recognized.  Since they do not cause a word break, they must be sepa‐
    rated from list by whitespace or another shell metacharacter.
```
10. Основываясь на предыдущем вопросе, как создать однократным вызовом `touch` 100000 файлов? А получилось ли создать 300000? Если нет, то почему?
```bash
vagrant@vagrant:~$ touch /tmp/{000001..100000}.tmp
-bash: /usr/bin/touch: Argument list too long
```
а так работает
```bash
vagrant@vagrant:~$ for i in {000001..100000}; do touch "/tmp/${i}.tmp"; done
vagrant@vagrant:~$ for i in {000001..300000}; do touch "/tmp/${i}.tmp"; done
```
12. В man bash поищите по `/\[\[`. Что делает конструкция `[[ -d /tmp ]]`
_Manual page bash(1) line 242/3993 7% (press h for help or q to quit)_
```bash
[[ expression ]]
    Return  a  status  of  0 or 1 depending on the evaluation of the conditional expression expression.  Expressions are composed of the
    primaries described below under CONDITIONAL EXPRESSIONS.  Word splitting and pathname expansion are not performed on the  words  be‐
    tween  the [[ and ]]; tilde expansion, parameter and variable expansion, arithmetic expansion, command substitution, process substi‐
    tution, and quote removal are performed.  Conditional operators such as -f must be unquoted to be recognized as primaries.

    When used with [[, the < and > operators sort lexicographically using the current locale.
```
```bash
vagrant@vagrant:~$ if [[ -d /tmp ]]; then echo "EXISTS"; fi
EXISTS
```
13. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:
```bash
    bash is /tmp/new_path_directory/bash
    bash is /usr/local/bin/bash
    bash is /bin/bash
```    
  
```bash
    vagrant@vagrant:~$ mkdir /tmp/new_path_directory
    vagrant@vagrant:~$ ln -s /bin/bash /tmp/new_path_directory/bash
    vagrant@vagrant:~$ export PATH=/tmp/new_path_directory:$PATH
```
14. Чем отличается планирование команд с помощью `batch` и `at`?
```bash
DESCRIPTION
       at and batch read commands from standard input or a specified file which are to be executed at a later time, using /bin/sh.

       at      executes commands at a specified time.

       batch   executes commands when system load levels permit; in other words, when the load average drops below 1.5, or the value specified  in
               the invocation of atd. 
```
15. Завершите работу виртуальной машины чтобы не расходовать ресурсы компьютера и/или батарею ноутбука.
```bash
    vagrant halt 
```
