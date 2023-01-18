# The "API Gateway service"

* From 1:35:30 in the [lecture video](https://www.youtube.com/watch?v=hmkF77F9TLw).

* Create the directory: `$ mkdir src/gateway`

## Set up the Python virtual environment

* Will use "pipenv" to create a Python "virtual environment"
  * NOTE: This is different from the video (he uses `$ python3 -m venv venv`)
  * See [How to use pipenv](docs/PART_2c_Python__Pipenv_and_Pipfile_for_dependencies.md)

* Create the "virtual env.": `$ pipenv --python 3.10`
  * => Creates the "Pipfile": /home/echobravo/DEV_NAV_KURS/KURS_freeCodeCamp__Microservices_Architecture/src/gateway/Pipfile
  * Check initial contents of "Pipfile": `$ more ./Pipfile`

* Launch a subshell in the Python "virtual environment": `$ pipenv shell`
  * Verify that the "environment variable" was set: `$ env | grep VIRTUAL`
  * => VIRTUAL_ENV=/home/echobravo/.local/share/virtualenvs/gateway-MTzm1DFj 

## Create the server.py file

* `$ touch server.py`
* Import the packages in "server.py": Video at 1:36:40.
* Install the Python dependencies into the "virtual environment".
  * NOTE: Remember to run `$ pipenv shell` first.
    * Exit the subshell later with `$ exit.`
  * NOTE: All packages will be added to "[packages]" section in "Pipfile".
  * `$ pipenv install jedi pika pymongo flask Flask-PyMongo`
    * NOTE: "pymongo" package contains "gridfs".
  * OPTIONAL: Only if you use "vim" as the editor: `$ pipenv install pylint`

## What is MongoDB GridFS?

* See [GridFS](https://www.mongodb.com/docs/manual/core/gridfs/) in the MongoDB manual.
* A specification for storing and retrieving files that exceed the BSON-document size limit of 16 MB.
  * BSON: Binary JSON.
* Allows files > 16MB: By "sharding" the files: stores each "chunk" as a separate document.
* A files is stored as 2 "collections": 1) The metadata, 2) The "chunks".

## Configure the RabbitMQ connection

* See video at: 1:44:30.

## How RabbittMQ fits in the overall architecture

* See video at: 1:45:40.
* Client uploads a video -> API Gateway -> Gateway stores the video in MongoDb.
  * -> User puts a message on the QUEUE that a video is ready to be processed
  * The "Video to MP3 converter service" listens to the QUEUE 
  * -> It gets the ID of the VIDEO from the message i nthe queue
  * -> Get the video from MongoDB -> Convert to MP3 -> Store MP3 on MongoDB
  * -> Put message on QUEUE that a conversion has been done
  * -> THe "Notification" service picks up the message from the QUEUE -> And sends an email to the User.
  * -> THe user uses the Id of the MP3 and JWT to request the API Gateway to download the MP3.
  * -> THe API Gateway pulls the MP3 from the MongoDB and serves it to "User".

## Key terms regarding "Microservice architectures"

* See [Key terms regarding "Microservice architectures"](./PART_5b_Microservices_key_terms_and_principles.md)

## Create login route for the "API Gateway" service

* Video at 1:52:40

## Create the "access" and "validate" Python modules (within the "Gateway API" folder)

* Pre-requisite: Install the "requests" package: `$ pipenv install requests`
  * => Make HTTP calls to other services.
* Will be created in a subdirectory of the "Gateway" service.

* `$ mkdir auth_svc; cd auth_svc`
* `$ touch __init__.py` => Will mark this directory as a Python "package"
* `$ touch access.py` => Creates the module that will contain our "login()" function.

## Overview of the authentication flow

* See video at 2:04:00
* auth/server.py:
  * "/login" route: Take email & pwd => Return a JWT token (JSON Web Token).
    * createJWT(): Part 1/3: Encrypts a payload (claims): username, exp, iat, "admin" (CUSTOM claim).
    * => Allow access to anyone with claim: "admin" = True
    * JWT Part 2/3: The secret.
    * JWT Part 3/3: The algorithm: "HS256"
  * "/validate" route:
    * Decoding the token: Use the same key ("JWT_SECRET") that we signed the JWT token with.

## Create the "upload()" function in the "storage" package ("util" module)

* See video at 2:13:00
* `$ cd gateway`
* `$ mkdir storage` : Name of the "package"
* `$ touch __init__.py` => Will mark this directory as a Python "package".
* `$ touch util.py` => Creates the "util" module that will contain our "upload()" function.

## How RabbitMQ works

* FIGUR: video at 2:17:00
* "Broker": Contains the "Exchange" and the "Queues".
* "Producer" sends message to the "Exchange". 
  * The "Exchange" routes the message to the right "Queue" based on some criteria.
  * We use the DEFAULT EXCHANGE, by coding this in Python: exchange="".
    * Every "Queue" is automatically bound to the DEFAULT EXCHANGE.
* => We will have 2 Queues: "video" and "mp3".
* "Consumer": Reads messages from Queues.

## "Competing Consumers Pattern" (in Message-oriented Systems)

* Video at 2:20:30:
* => Multiple "Consumers" can consume messages from the same "Queue".
* => Scaling: Higher throughput.
* => Enables parallell processing of uploaded videos.

## Create a Kubernetes "Deployment" for the "API Gateway" service

* Video at 2:26:15
* `$ cd gateway`
* Copy the contents of "auth/Dockerfile" into "gateway/Dockerfile":
  * `$ cp ../auth/Dockerfile ./Dockerfile`
* Changes in "Dockerfile"
  * Change port to: `EXPOSE 8080`: Will be port of the "API Gateway".
  * Remove `default-libmysqlclient-dev` from the "apt-get" command line.

* Create "requirements.txt" (needed by Python) by running: `$ pipreqs .`
  * => OUTUT: "INFO: Successfully saved requirements file in ./requirements.txt"
  * NOTE: See further explanation of "pipreqs" etc. in ".gateway/Dockerfile".
* ALT. 1: Build image with Docker: 
  * `$ docker build .`
  * `$ docker images` => Find the "IMAGE ID".
  * `$ docker tag d8c45338a4ce gateway:latest` => Tag the "gateway" image.
  * Remove the image: `$ docker image remove gateway:latest`

* ALT. 2: Build image using "minikube":
  * Instead of using `$ docker push` (which is used in the video at 2:28:10):
    * => We instead build and load the Docker image directly into minikube's image registry using the `$ minikube image build ...` command
  * REMINDER: First exit the "Python virtual environment" subshell (created by running `$ pipenv shell` earlier):
    * By running `$ exit`.
  * `$ minikube start`
  * Check existing images: `$ minikube image ls`
    * => "docker.io/library/auth:latest"
    * => "docker.io/library/hello-world:latest"
  * `$ minikube start`
  * `$ minikube image build -t gateway .` => Build the image based on "./Dockerfile"
  * `$ minikube image ls` => Show all images in "minikube" registry
    * => "docker.io/library/gateway:latest"

## Create the Kubernetes "Deployment" (manifest files: yaml)

* See video at 2:29:00

* `$ mkdir manifests` and `$ cd manifests`

* THere are 3 alternatives to create the yaml files:
  * 1) Create from scratch: `$ touch gateway-deploy.yaml` (see video).
  * 2) Copy from "auth" service: `$ cp ../../auth/manifests/auth-deploy.yaml gateway-deploy.yaml`
    * => Replace all "auth" with "gateway" in the yaml
  * 3) Copy yaml from "repo": <https://github.com/selikapro/microservices-python/blob/main/src/gateway/manifests/gateway-deploy.yaml>
  
* USEFUL: To remove an image from the "minikube image registry":
  * `$ minikube image rm docker.io/gateway/latest:latest`

* Create the "ConfigMap" yaml:
  * `$ touch configmap.yaml`
  * Copy from repo: <https://github.com/selikapro/microservices-python/blob/main/src/gateway/manifests/configmap.yaml>
  * => The following env. var. is set: `AUTH_SVC_ADDRESS: "auth:5000"`

* Create the "Secret" yaml:
  * `$ touch secret.yaml`
  * Copy from repo: <https://github.com/selikapro/microservices-python/blob/main/src/gateway/manifests/secret.yaml>

* Create the "Service" yaml:
  * `$ touch service.yaml`
  * Copy from repo: <https://github.com/selikapro/microservices-python/blob/main/src/gateway/manifests/service.yaml>

## INGRESS: "Gateway API": Configure access from outside of the cluster

* See video at 2:32:30
* Create another Kubernetes configuration:
  * => Create an "ingress" to route "external" traffic to the "Gateway API" service.
  * Will allow HTTP traffic from outside of the cluster to access the "API Gateway" endpoints.
  
* `$ touch ingress.yaml`
* Copy the file contents from the repo: <https://github.com/selikapro/microservices-python/blob/main/src/gateway/manifests/ingress.yaml>

## What is an "INGRESS" in the context of a Kubernetes cluster?

* See video at 2:33:15.
  * Nice illustration: Kubernetes: Pods, Service, Labels.

* "Service" (Kubernetes)
  * Bind to Pods using "Selectors": E.g a LABEL named "app=A":
    * => It is the "Labels" that binds each individual "Pod" to its "Service".

* Service (and its Pods) sits in a "Cluster": which is our "private network".
  * Gateway: 1.1.1.1 (load balances btwn. the Pods)
  * Pods: 10.10.10.1 ... 10.10.10.3

* "Ingress Controller"
  * Has a "load balancer" that is the entrypoint to our "Cluster" (Service & Pods).
  * Has a set of "Rules": specifies which request goes where.
    * Maps an external IP-adress (e.g. mp3converter.com) to the internal cluster IP of our "API Gateway" service (1.1.1.1)

## Write the ingress.yaml" file

* See video at 2:36:00
* Will use an "nginx" ingress (default).
* Allow any "file size" by setting the "body-size" annotation on nginx to 0.
* Also set the read and send timeouts.
* Specifying the external DNS name: `host: mp3converter.com`
  * NOTE: Need to map "mp3converter.com" to "localhost" on our local machine (see below).
    * This is needed when we test on "minikube".
  * => Also need to TUNNEL all the requests made to "localhost" to "minkube", using `$ minikube tunnel`

* Map "mp3converter.com" to "localhost" in WSL:
  * `$ sudo nano /etc/hosts`
  
  * Add this line: `127.0.0.1 mp3converter.com`
    * => Any request to "mp3converter.com" will be routed to the "loopback address" (= "localhost").
    * Verify with: `$ ping mp3converter.com` => Will output "64 bytes from localhost (127.0.0.1): ..."

* Configure a "minikube" add-on to allow INGRESS:
  * `$ minikube addons list`
  * `$ minikube addons enable ingress`
    * NOTE: The "ingress" addon is OFFICIAL => It is maintained by Kubernetes.
  
  * Now run `$ minikube tunnel`:
    * => All ingress resources will be available at "127.0.0.1" ("localhost").
    * NOTE: "Do not close the terminal (Ctrl+C) because it's process must stay alive for the tunnel to be accessible".
    * => Any request to "localhost"
      * => Will be routed to our minikube cluster via the "ingress".
  * Run `$ k9s`, press "0":
    * => Two (One?) "ingress-nginx" pods are now showing as Running.

* Finally, deploy the "gateway" service to Kubernetes
  * `$ cd gateway/manifests`
  * `$ kubectl apply -f ./`
  * `$ k9s` => The "gateway" pods have errors:
    * Because RabbitMQ setup is NOT complete.
  * => Scale down the Deployment of the "gateway" service to "0" replicas:
    * `$ kubectl scale deployment --replicas=0 gateway`
    * OR: Delete all resources: `$ kubectl delete -f ./`

## NEXT: Create a RabbitMQ image and deploy to Kubernetes

* See [Create a RabbitMQ image and deploy to Kubernetes](PART_6_Create_a_RabbitMQ_image_and_deploy_to_Kubernetes.md)