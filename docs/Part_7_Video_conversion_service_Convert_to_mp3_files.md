# Service to convert video messages into MP3 files

* See video at: 03:07:45
  
* Service overview:
  * Pulls messages from the "video" queue (added by "Gateway" service)
  * Convert the video into an mp3 file.
  * Store the mp3 in mongodb.
  * Put a message on the RabbitMQ "mp3s" queue.

## Create the "Converter" service

* NOTE: This is a "consumer" service wrt. the "videos" message queue

* `$ mkdir src/converter`
* `$ cd src/converter`
* `$ touch consumer.py`
* Edit the file as shown in video at "03:08:00"

## Create Python virtual environment, install dependencies and create "requirements.txt"

### Create a Python "virtual environment"

* See details: "[Use pipenv to create a Python virtual environment](./PART_2c_Python__Pipenv_and_Pipfile_for_dependencies.md)"

* Create a Python "virtual environment" for the "Converter" service: `$ pipenv --python 3.10`
  * => Creates `./Pipfile`
  * OUTPUT: Virtualenv location: `/home/echobravo/.local/share/virtualenvs/converter--FAceqUC`

### Activate the Python "virtual enviroment"

* Run `$ pipenv shell`
  * => "Launching subshell in virtual environment..."
* Verify that it was activated: `$ env | grep VIRTUAL`

### Install the "consumer.py" Python dependencies in the "virtual environment"

* See video at "03:17:00"
* `$ pipenv install pika pymongo`
* Verify that they are now listed under "[packages]" section: `$ more Pipfile`

### Dependencies: Use "Pipfile" to create "requirements.txt"

* The course refers to "requirements.txt" inside "Dockerfile" for the list of Python dependencies.
  * This might be an "older" way of handling "dependencies".
  * See details of "requirements.txt" [here](./PART_3_Deploy_the_auth_service_using_Docker_and_Kubernetes.md)
  * Also see further explanation of "pipreqs" etc. in `src/gateway/Dockerfile`.
  * Repo of [pipreqs](https://github.com/bndr/pipreqs) : 
    * _"Generate pip requirements.txt file based on imports of any project"_

* Create "requirements.txt" from "Pipfile": `$ pipreqs .`
  * => OUTPUT: "INFO: Successfully saved requirements file in ./requirements.txt"

* Verify that all dependencies are listed: `$ more requirements.txt`

### Finally, exit the Python "virtual environment" subshell

* Run `$ exit`

## Create the "convert" package

* See video at "03:17:20"
* Create the Python package: `$ mkdir convert`
* `$ touch __init__.py`
* Create the Python "module": `$ touch to_mp3.py`
* Edit the contents of `to_mp3.py` (see video or repo).
* Add the new Python dependency: `$ pipenv install moviepy`
  * NOTE: First start the "virtual envirnment" with `$ pipenv shell`.
  * Generate "requirements.txt" again: `$ pipreqs --force .`

## Create the "Dockerfile" for the service

* See video at "3:31:30"
* Copy contents from the "[Dockerfile](https://github.com/selikapro/microservices-python/blob/main/src/converter/Dockerfile)" in the repo.
* Build the image using "minikube": `$ minikube image build -t converter .`
  * => Image is tagged "converter:latest" 
* List the minikube registry images: `$  minikube image ls`
  * => Image is listed as "docker.io/library/converter:latest"

## Create the Kubernetes "mainfest" files

* Se video at "3:33:45".
* `$ mkdir mainfests`
* Copy the contents of all the "manifest" files from the repo:
  * "[configmap.yaml](https://github.com/selikapro/microservices-python/blob/main/src/converter/manifests/configmap.yaml)"
  
  * "[converter-deploy.yaml](https://github.com/selikapro/microservices-python/blob/main/src/converter/manifests/converter-deploy.yaml)"
    * Replace this line: `image: sweasytech/converter` with `image: converter`
    * Add this line after: `imagePullPolicy: Never`
      * So that images are not downloaded from internet, but searched for in local image registry.

  * "[secret.yaml](https://github.com/selikapro/microservices-python/blob/main/src/converter/manifests/secret.yaml)"
  
## Add the "mp3s" queue using RabbitMQ manager

* Video at "03:36:40".
* See details [here](PART_6_Create_a_RabbitMQ_image_and_deploy_to_Kubernetes.md)

* Make sure the "RabbitMQ" service is running:
  * Check with `$ kubectl get pods`
  * If not running, from "manifests" folder run: `$ kubectl apply -f ./`

* Make the port of the "RabbitMQ service" available on port 80:
  * `$ kubectl port-forward rabbitmq-0 80:15672`

* Log on to the "Rabbit MQ Admin" GUI:
  * Open in browser: <http://localhost>
  * Log on with: USER/PWD: `guest`/`guest`
  * Go to the "Queues" TAB: <http://localhost/#/queues>
  * Add a "Durable" queue named "mp3s" (on the Queues TAB).

## Start the "mp3Converter" service in Kubernetes

* Go to the "manifests" folder.
* Start service by running: `$ kubectl apply -f ./`
* Check status of pods with `$ kubectl get pods`
* Or, check using `$ k9s`
* If errors => See logs with: `$ kubectl logs -f converter-f5476f68c-f5lzh`
  * NOTE: Choose one of the Pod "NAME"s listed.
  * NOTE: "-f" means "follow".
* 

## NEXT: Test video upload and verify conversion to mp3

* See [Test video upload and verify conversion to mp3](./Part_8_Test_video_upload_and_verify_conversion_to_mp3.md)