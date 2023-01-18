# INSTALL: MySQL (On Ubuntu 22.04 and WSL2)

## Resulting CONFIGURATION: MySQL

* USER: root
  * PWD: Tarmslyng_112
  
* Log on:
  * $ mysql -u root -p
  * $ mysql --user=root --password=Tarmslyng_112

* MySQL configuration file:
  * /etc/mysql/my.cnf

* "systemd" service file for MySQL:
  * /lib/systemd/system/mysql.service

* "mysqld" will log errors to:
  * /var/log/mysql/error.log

## INSTALLATION: MySQL

* "How to Install MySQL on Ubuntu 22.04"
  * https://linuxhint.com/install-mysql-on-ubuntu-22-04

* INSTALL:
  * > $ sudo apt-get install mysql-server
  
* Verify "systemd" service has started:
  * `$ systemctl is-active mysql`
  * `$ systemctl status mysql`
  * `$ systemctl --failed`
  * `systemctl status mysql`

## EXTRA CONFIGURATION STEP:

* DOES NOT WORK => SKIPPED!
  * Performing an initial and interactive configuration of the MySQL server:
  * > $ sudo mysql_secure_installation
 
* Log in to "mysql"
  * > $ sudo mysql
  
* Change PWD of "root": 
  * > ALTER USER 'root'@'localhost'  IDENTIFIED WITH mysql_native_password BY 'Tarmslyng_112';
  * > exit

* Log on with PWD
  * > $ sudo mysql --user=root --password=Tarmslyng_112
  
## Disable password validation

* If you get _"ERROR 1819 (HY000) at line 1: Your password does not satisfy the current policy requirements"_
* => Run this command: `mysql> UNINSTALL COMPONENT 'file://component_validate_password';`
* This will disable password validation.
