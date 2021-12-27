# Курсовая работа по итогам модуля "DevOps и системное администрирование"

- Процесс установки и настройки ufw
```bash
vagrant@vagrant:~$ sudo apt-get update && sudo apt-get install ufw -y
...
vagrant@vagrant:~$ ufw version
ufw 0.36
Copyright 2008-2015 Canonical Ltd.
vagrant@vagrant:~$ sudo ufw status
Status: inactive
vagrant@vagrant:~$ sudo ufw allow ssh/tcp
Rules updated
Rules updated (v6)
vagrant@vagrant:~$ sudo ufw allow https/tcp
Rules updated
Rules updated (v6)
vagrant@vagrant:~$ echo 'y' | sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? Firewall is active and enabled on system startup
vagrant@vagrant:~$ sudo ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
22/tcp (v6)                ALLOW IN    Anywhere (v6)
443/tcp (v6)               ALLOW IN    Anywhere (v6)
80/tcp (v6)                ALLOW IN    Anywhere (v6)
```

- Процесс установки и выпуска сертификата с помощью hashicorp vault
```bash
vagrant@vagrant:~$ curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
OK
vagrant@vagrant:~$ sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
...
Fetched 41.1 kB in 1s (28.0 kB/s)
Reading package lists... Done
vagrant@vagrant:~$ sudo apt-get install vault
Reading package lists... Done
...
Unpacking vault (1.9.2) ...
Setting up vault (1.9.2) ...
Generating Vault TLS key and self-signed certificate...
Generating a RSA private key
..........++++
...............................................................................................................................................................................................................++++
writing new private key to 'tls.key'
-----
Vault TLS key and self-signed certificate have been generated in '/opt/vault/tls'.

vagrant@vagrant:~$ export VAULT_ADDR=http://127.0.0.1:8200
vagrant@vagrant:~$ export VAULT_TOKEN=root
vagrant@vagrant:~$ vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
vagrant@vagrant:~$ vault write -field=certificate pki/root/generate/internal \
>      common_name="example.com" \
>      ttl=87600h > CA_cert.crt
vagrant@vagrant:~$ vault write pki/config/urls \
>      issuing_certificates="$VAULT_ADDR/v1/pki/ca" \
>      crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls
vagrant@vagrant:~$ vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=43800h pki_int
Success! Tuned the secrets engine at: pki_int/
vagrant@vagrant:~$ vault write -format=json pki_int/intermediate/generate/internal \
>      common_name="example.com Intermediate Authority" \
>      | jq -r '.data.csr' > pki_intermediate.csr
vagrant@vagrant:~$ vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
>      format=pem_bundle ttl="43800h" \
>      | jq -r '.data.certificate' > intermediate.cert.pem
vagrant@vagrant:~$ vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed
vagrant@vagrant:~$ vault write pki_int/roles/example-dot-com \
>      allowed_domains="example.com" \
>      allow_subdomains=true \
max_ttl>      max_ttl="744h"
Success! Data written to: pki_int/roles/example-dot-com
```
~/new_cert.sh - Скрипт генерации приватного ключа и сертификата сервера NGINX
```bash
#!/usr/bin/env bash
vault write -format=json pki_int/issue/example-dot-com common_name="test.example.com" ttl="744h" > cert.json
jq -r '.data.private_key' ./cert.json > ./ssl/test.example.com.key
jq -r '.data.certificate' ./cert.json > ./ssl/test.example.com.crt
sudo service nginx restart
```
- Процесс установки и настройки сервера nginx
```bash
vagrant@vagrant:~$ sudo apt-get install nginx -y
vagrant@vagrant:~$ sudo vi /etc/nginx/sites-available/default
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        # SSL configuration
        **listen 443 ssl default_server;
        listen [::]:443 ssl default_server;**
        #

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        **server_name test.example.com;
        ssl_certificate     /home/vagrant/ssl/test.example.com.crt;
        ssl_certificate_key /home/vagrant/ssl/test.example.com.key;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;**
```
- Страница сервера nginx в браузере хоста не содержит предупреждений 
[test.example.com](https://disk.yandex.ru/i/I1KS412vOz57Cw)
- Скрипт генерации нового сертификата работает (сертификат сервера ngnix должен быть "зеленым")
```bash
#!/usr/bin/env bash
vault write -format=json pki_int/issue/example-dot-com common_name="test.example.com" ttl="744h" > cert.json
jq -r '.data.private_key' ./cert.json > ./ssl/test.example.com.key
jq -r '.data.certificate' ./cert.json > ./ssl/test.example.com.crt
sudo service nginx restart
```
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)
```bash
vagrant@vagrant:~$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# m h  dom mon dow   command
16 10 * * * /home/vagrant/new_cert.sh >/dev/null 2>&1
vagrant@vagrant:~$ grep CRON /var/log/syslog
...
Dec 27 10:16:01 vagrant CRON[1813]: (vagrant) CMD (/home/vagrant/new_cert.sh >/dev/null 2>&1)
```
