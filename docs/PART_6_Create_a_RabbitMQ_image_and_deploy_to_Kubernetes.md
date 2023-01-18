# Create a RabbitMQ image and deploy to Kubernetes
  
* Se video at 2:43:30: <https://www.youtube.com/watch?v=hmkF77F9TLw>

## Configure RabbitMQ as a StatefulSet in Kubernetes

* GOAL: Create it as a StatefulSet
  * => Messages persists => Data are available after a restart / crash.
* A Kubernetes StatefulSet:
  * Each pod has a "persistent ID" that is maintained across any rescheduling.
  * => Makes it possible to use the SAME volume (storage) when restarting a pod.

* Copy all the yaml files from the repo

  * `$ mkdir src/rabbit; cd rabbit`
  * `$ mkdir manifests; cd manifests`
  * Copy all the "yaml" files for the "rabbit" service into the "manifests" folder.
  * `$ touch configmap.yaml ingress.yaml pvc.yaml secret.yaml service.yaml statefulset.yaml`
  * Then copy the file contents from the repo: <https://github.com/selikapro/microservices-python/tree/main/src/rabbit/manifests>
* `statefulset.yaml`
  * volumeMounts: Specify a persistent folder for the pod.
  * PVC: "Persistent Volume Claim". Video at 2:48:10.

## Define a hostname for the "RabbitMQ GUI port" on WSL
  
* See video at: 2:57:30
* `$ sudo nano /etc/hosts`
* Add this line: `127.0.0.1 rabbitmq-manager.com`
* Verify with `$ ping rabbitmq-manager.com`

## Define Windows "DNS hostnames" that refer to the "WSL IP address" (dynamic)

* WHY? To be able to use DNS hostnames e.g. in a browser that maps to the (dynamic) "WSL IP address".
  * NOTE: The "WSL IP address" changes between each shutdown of WSL.
* See [Define "DNS hostnames" in Windows that refer to the "WSL IP address"](Part_6b_Define_Windows_DNS_hostnames_that_refer_to_the_dynamic_WSL_IP_address.md)

## Deploy RabbitMQ to Kubernetes

* `cd src/rabbit/manifests`
* `$ kubectl apply -f ./`
* `$ k9s` => Verify that 1 "rabbitmq" pod is running.

* USEFUL "kubectl" commands
  * DEBUGGING: `$ kubectl describe pvc` => Outputs debug info for the "pvc"
  * DELETE all resources created by a deployment: `$ kubectl delete -f .`

## Open the "RabbitMQ Manager" GUI from a browser in Windows

* NB! Configured the "DNS hostname" in "/etc/hosts" (see above).
  * And gave access to port using an "Ingress" (see above).

* Open the port to the "Rabbit MQ Service"
  
  * NOTE: The video instructions DID NOT WORK (3:02:40):
    * => DOES NOT WORK: `$ minikube tunnel`
  
  * => HAD TO RUN THIS INSTEAD: `$ kubectl port-forward rabbitmq-0 80:15672`
    * => OUTPUT: `Forwarding from 127.0.0.1:80 -> 15672`
    * => OUTPUT `Forwarding from [::1]:80 -> 15672`

* Open the RabbitMQ GUI in a browser:

  * ALTERNATIVE 1: Open a browser in Windows and access the GUI with URL: `localhost` or `127.0.0.1`
    * NOTE: "Windows" will automatically map "localhost" and "127.0.0.1" to these ports on a running "WSL" Linux instance.

  * ALTERNATIVE 2: Define and use "DNS hostnames" instead:
    * First, add the "DNS hostname" into ``~/.wsl2hosts` as described [here](Part_6b_Define_Windows_DNS_hostnames_that_refer_to_the_dynamic_WSL_IP_address.md):
      * Map "rabbitmq-manager.com" to "ubuntu.wsl".
    * Restart the "WSL2 Host service" as described [here](Part_6b_Define_Windows_DNS_hostnames_that_refer_to_the_dynamic_WSL_IP_address.md).
    * Verify that hostname is accessible from Windows by running `> ping rabbitmq-manager.com` from Powershell.
    * Open a browser in Windows and access the GUI with URL: <http://rabbitmq-manager.com>

## Log on to the "RabbitMQ Manager" GUI and Define 2 queues

* Log on with the default USER for the "Rabbit MQ Admin" GUI:  
  * USER: `guest`
  * PWD: `guest`
  * Go to the "Queues" TAB: <http://localhost/#/queues>

## Define the "video" queue in "RabbitMQ Manager"

* See video at "[3:04:00](https://www.youtube.com/watch?v=hmkF77F9TLw)".
* Log on "RabbitMQ" (see above).
* Go to the "Queues" TAB: <http://localhost/#/queues>
* Queue 1: "video"
  * See name of "queue" in source file `src/gateway/storage/util.py`
  * Set "Name" to "video"
  * Set "Curability" to "Durable"
    * => The queue will be persistent across container/pod restarts.

## USEFUL: Sequence of commands to start up `minikube` with the project's "Rabbit MQ" pods

```bash
minikube status
minikube start
kubectl get po -A

# 1) Start the "Authentication" pods:
cd src/auth/manifests
kubectl apply -f ./  # Starts 2 pods.

# 3) Start the "Gateway"" pods:
cd src/gateway/manifests
kubectl apply -f ./

# 3) Start the RabbitMQ pods:
cd src/rabbit/manifests
kubectl apply -f ./

# Verify that the follwoing pods are running:
#   1) 2 "auth" pods. 
#   2) 2 "gateway" pods. 
#   3) 1 "rabbitmq" pod.
k9s # Then press "0" to see all. 
# Alternative to using "k9s": 
kubectl get pods # Lists all your pods.

# => If some service has Errors, then remove it's pods with: 
kubectl delete -f ./

# NOTE: Needed since "minikube tunnel" DID NOT WORK:
kubectl port-forward rabbitmq-0 80:15672
# => Output: "Forwarding from 127.0.0.1:80 -> 15672"

# Then open "Rabbit MQ Manager": http://localhost (user/pwd: guest/guest)
#    NOTE: This must be in a browser in Windows (not in WSL).
```

## USEFUL: How to re-build the image of a Python service

* Background:
  * We can use `minikube image build ..` directly!
    * NOTE: Instead of using `$ docker push ` (video at 2:28:10):
  * => The image is loaded directly into "minikube" from our "local" Docker image.
  
* Clean up tasks:
  * First run `$ exit` to exit the "Python virtual environment" subshell.
  * NOTE: The Python "virtual environment" was created by running `$ pipenv shell` earlier.

* Minikube first needs to be started: `$ minikube start`

* List all images in the minikube registry: `$ minikube image ls`
  * "docker.io/library/auth:latest"
  * "docker.io/library/gateway:latest"
  * "docker.io/library/hello-world:latest"

* Example: Build the image for the "Gateway" service:
  * `$ cd src/gatway`  # Location of "Dockerfile"
  * `$ minikube image build -t gateway .`
    * => Builds the image based on "./Dockerfile"
    * => Will be tagged "gateway:latest"
  * `$ minikube image ls`
    * => Lists all images in the "minikube" registry.
    * => "docker.io/library/gateway:latest"

* To remove the "gateway" image from the "minikube" registry:
  * NOTE: Must first stop the pods of the service:
    * Run this inside the "manifests" folder:
      * `$ kubectl delete -f ./`
    * Verify all pods are stopped with: `$ kubectl get pods`
  * `$ minikube image rm docker.io/library/gateway:latest`

* NEXT: [Service to convert video messages into MP3 files](./Part_7_Video_conversion_service_Convert_to_mp3_files.md)