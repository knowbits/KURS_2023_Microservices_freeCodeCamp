# Basic installation: minikube, MySQL, python

## INSTALL basic tooles for local Kubernetes cluster

$ minkube start
  
* minikube uses CONFIG file: 
  * /home/echobravo/.kube/config

$ minikube addons enable metrics-server

$ kubectl get po -A   # List pods.

$ k9s # Then choose: "<0> all" : To see all running pods.

## INSTALL MySQL
* See [Install MySQL on Ubuntu/WSL2](docs/KURS_freeCodeCamp_PART_1b_Install_MySQL_on_Ubuntu_and_WSL2.md)
  
* => MySQL will run as a "systemd" service. 
  * Verify with: `$ systemctl status mysql.service`

* USER/PWD of "mysql":
  * USER: root
  * PWD: Tarmslyng_112

* Log on to MySQL server:
  * $ mysql -u root -p  # => Type in the PASSWORD in the console...
  * $ mysql --user=root --password=Tarmslyng_112

