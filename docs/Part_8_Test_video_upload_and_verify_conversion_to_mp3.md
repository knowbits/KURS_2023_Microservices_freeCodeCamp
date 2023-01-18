# Test video upload and verify conversion to mp3

* Video at "3:41:30".


## PRE-REQUISITES: Open the "RabbitMQ Manager" GUI

* Make sure the "RabbitMQ" service is running:
  * Check with `$ kubectl get pods`
  * If not running, from "manifests" folder run: `$ kubectl apply -f ./`

* Make the port of the "RabbitMQ service" available on port 80:
  * `$ kubectl port-forward rabbitmq-0 80:15672`
  * NOTE: "minikube tunnel" does not work, for some reason..
    * => Have to use "port-forward" instead.

* Open "RabbitMQ GUI" in browser: <http://localhost>
  * Log on with: USER/PWD: `guest`/`guest`

* Go to the "Queues" TAB: <http://localhost/#/queues>

## Download a video file from Youtube

* Install a "Youtube downloader": `$  sudo apt install youtube-dl`

* Get a link to a Youtube video:
  * Go to video "Sample Videos _ Dummy Videos For Demo Use" and Press "Share" + "Copy".
  * The link is: <https://youtu.be/EngW7tLk6R8>

* Go to tmp folder: `$ cd /tmp/`: 
* Download the video: `$ youtube-dl --format mkv https://youtu.be/EngW7tLk6R8`

* Rename the video file:
  * `$ mv "Sample Videos _ Dummy Videos For Demo Use-EngW7tLk6R8.mp4" video_file.mkv`

## Get user credentials from the "mysql" database

* `$ mysql --user=root --password=Tarmslyng_112`
* `mysql> use auth;`
* `mysql> show tables;`
* `mysql> select * from user;`

  ```csv
    id | email             | password
    ---------------------------------
    1  | georgio@email.com | Admin123
  ```

* Will use these credentials (user/pwd) to verify HTTP requests from a user:
  * This is done in the "login" endpoint in the "auth" service.
  * => The "auth" service will then create and return a JWT token that user can use in the following HTTP request to upload a video.

## Upload video by using "HTTPie" (instead of "curl")

* See video at "3:45:20".
* How to use the `http` tool of "HTTPie":
  * See either `$ tldr http` or * `$ man http`
* Fix error in 2 Python files:
  * See video at "3:47:45".
  * Change all occurrences (2) of `response.txt` to `response.text`
  * File 1: `src/gateway/access_svc/access.py`
  * File 2: `src/gateway/auth/validate.py`
* Rebuld the image for "gateway" service:
  * `$ cd src/gateway/manifests`
  * `$ kubectl delete -f ./`
  * `$ cd src/gateway`
  * `$ minikube image build -t gateway`
* Restart the "gateway" service:
  * `$ cd src/gateway/manifests`
  * `$ kubectl apply -f ./`
  * Verify pods are running: `$ kubectl get pods`

## Fixing the ERROR: => Have to run MySQL in Kubernetes instead of WSL/Ubuntu

* => Get an ERROR when trying to generate a JWT:
  * See video at "3:49:40".
  * Fails:
    * `$ curl -X  POST http://mp3converter.com/login -u georgio@email.com:Admin123`

* => DEBUG: Print logs of pods
  * Get running pods:`$ kubectl get pods -o wide`  `$ kubectl get pods`
  * Print log of a pod: `$ kubectl logs auth-7976c59bb7-jsrks`

* => DEBUG: Print environment variables of the "auth" pod
  * Get running pods:`$ kubectl get pods -o wide`  `$ kubectl get pods`
  * Log in: `$ kubectl exec --stdin --tty auth-7976c59bb7-jsrks -- bash`
  * Print the env. vars.: `root@auth-7976c59bb7-jsrks:/app# env | grep MYSQL`

* SOLUTION: Had to run MySQL as a pod in Kubernetes
  * I descripbed the solution in the repo "Issues" here: 
    * <https://github.com/selikapro/microservices-python/issues/16#issuecomment-1374903406>

=> Here is my solution (copied from the repo):

> Same error. `MySQLdb.OperationalError: (2005, "Unknown MySQL server host 'mysql' (-3)")`

Been having the same MySQL connection problems, @kshitizJ. 

Finally got it working, the JWT is now returned (!) when calling:
   curl -X  POST http://mp3converter.com/login -u georgio@email.com:Admin123

I suspect that trying to access a MySQL db installed in Windows/WSL/Ubuntu using "host.minikube.internal" might be the culprit. Solution:  Run MySQL in Kubernetes as @selikapro suggested.

1. Follow the instructions above by @selikapro and run mysql in the cluster, so create the "pod.yaml" as described above.
2. NOTE: There is typo in that "pod.yaml", change "Aauth123" to "Auth123"
3. Then create a "service.yaml" file to expose the mysql pod as a service, so that it can be called using "mysql" from other pods in the cluster. See below. 
4. I also had to make one more change in "pod.yaml": replace 'localhost' with '172.17.0.1'

PS! You might need to add a label to "pod.yaml", to be able to refer to it from "service.yaml":

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mysql
  labels:
    app: mysql
# Only the last two lines were added.
# Rest of file not included..
```

The "service.yaml":

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  selector:
    app: mysql
  type: ClusterIP
  ports:
    - port: 3306
      targetPort: 3306
      protocol: TCP
```

* USEFUL: To test mysql running in Kubernetes
  * `$ kubectl port-forward mysql 7777:3306`
  * `$ mysql --user=auth_user --password=Auth123 --port=7777`

## RESUMING the video: Generate a JWT

* See video at "3:49:45".
* Steps to generate the JWT:
* `$ minikube start`
* Start all the services with `$  kubectl apply -f ./`
* Verify that servces are running with: `$ kubectl get pods`
* `$ minikube tunnel`
* `$ curl -X  POST http://mp3converter.com/login -u georgio@email.com:Admin123`
  * => JWT: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imdlb3JnaW9AZW1haWwuY29tIiwiZXhwIjoxNjczNjA0NjIxLCJpYXQiOjE2NzM1MTgyMjEsImFkbWluIjp0cnVlfQ.WYMG0NJsNay2huObaue8ZSOuYbMyBlqO0H2ZLqhumiE`
    * NOTE: Remove the `%` at the end of the JWT. 

## Upload the video file
* NOTE: See download steps above.
* Go to the folder where the video file was downloaded:
  * `$ cd /tmp/`

* Upload the video using a "Bearer" token (the newly generated JWT):
  * curl -X POST -F 'file=@/tmp/video_file.mkv' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imdlb3JnaW9AZW1haWwuY29tIiwiZXhwIjoxNjczNjExMzE2LCJpYXQiOjE2NzM1MjQ5MTYsImFkbWluIjp0cnVlfQ.jjOgMciWSAmwjVYVp2qy1WyNSwDH7gvyt1IPZROIGEk' http://mp3converter.com/upload

* => Get ERRORs..

## DEBUGGING: Make it easier to look at logs for each service

* Scale all Pods down to 1 instance:
  * "gateway" service: `$  kubectl scale deployment --replicas=1 gateway`
  * "auth" service: `$  kubectl scale deployment --replicas=1 auth`
  * "converter" service: `$  kubectl scale deployment --replicas=1 converter`

* Stream the logs of each Pod (-f)
  * Open a terminal window for each service: auth, gateway, converter
  * Get the pod names: `$ kubectl get pods`
  * `$ kubectl logs -f auth-7976c59bb7-cs8cd`
  * `$ kubectl logs -f gateway-65d86499b9-4hrzx`
  * `$ kubectl logs -f gateway-65d86499b9-4hrzx`

## Try again: Upload video I

* See video at "3:56:50".

* Repeat the `$ curl POST` command from above.
  * => Getting the ERROR: `internal server error%`
  * The logs reveal that the "gateway" service returns a `500` ("500 Internal Server Error").

* Edit the file `src/gateway/storage/util.py`
  * In the `def upload()` function add line: `print(err)` after each `except` line.

* DEBUGGING:
  * Print the logs of each pod: `kubectl logs "pod-name-here"`

* => This did also NOT resolve the issue.
* SOLUTION: MongoDB also needs to be run in Kubernetes, because "minikube" on WSL/Ubuntu is unabe to resolve the hostname `host.minikube.internal`

## Set up MongoDB to run in Kubernetes

* See steps in "[Part 8b: Set up MongoDB to run in Kubernetes](Part_8b__Set_up_MongoDB_to_run_in_Kubernetes.md)"

## Try again: Upload video II

* Repeat the `$ curl POST` command from above.
  * => Still getting the ERROR: `internal server error%`

* => This did NOT resolve the issue.
  
* __SOLUTION: The "gateway" service needed to be restarted!__
  * WHY? Because it was no longer properly connected to the "rabbitmq" service.
  * See his explanation at "4:00:30" in the video.

## Verify that the uploaded video is converted into mp3

* See video at "4:12:45".
* Verify existence of mp3 files using the "RabbitMQ Manager":
  * Forward the RabbitMQ port: `$ kubectl port-forward rabbitmq-0 80:15672`
  * Open browser at: <http://localhost:80>. Log on with "guest/guest".
  * Go to "Queues" tab. Check that the "mp3s" ques has files in it. 

* Verify existence of mp3 files using the `mongosh` client tool:
  * Log on to the shell of the "mongodb" service:
    * `$ kubectl exec service/mongo -it -- /bin/bash`
  * Run `# mongosh` in the container's shell.
  * Run these "mongodb" database commands:
    * `> show databases;`
    * `> use mp3s;`
    * `> show collections;`
      * => Lists the following (GridFS):
      * `fs.files`: The file meta-data
      * `fs.chunks`: The file data (stored in chunks)
    * `> db.fs.files.find();`
      * => Lists meta-data about all files in "mp3s" database.
  * Copy the `ObjectId` of one of the mp3 files listed, e.g. `"63c47dc3e2a97d508f7e75b9"`.

## Download the mp3 file from "mongodb" to verify the audio

* See video at "4:15:40".
* Forward the port of the "mongodb" pod:
  * Get the POD NAME: `$ kubectl get pods`
  * Get the port: `$ kubectl get pod mongo-869f6488c8-vk9rj --template='{{(index (index .spec.containers 0).ports 0).containerPort}}{{"\n"}}'`
    * => "27017"
  * Forward the Pod's port: `$ kubectl port-forward mongo-869f6488c8-vk9rj 27017:27017`

* NOTE: If needed, install "mongodb" on Ubuntu: includes the client CLI tools
  * `$ sudo apt install -y mongodb-org`
  * This includes client tools like `mongosh`, `mongofiles`.  
  * Verify that "mongod" daemon is not running as a "systemd" service:
    * Check status: `$ systemctl status mongod`
    * Run if "mongod" was enabled: `$ sudo systemctl disable mongod`

* Use the `mongofiles` tool to get the "mp3" and save to a local in your shell:
  * `$ mongofiles --db=mp3s get_id --local=test.mp3 '{"$oid": "63c47dc3e2a97d508f7e75b9"}'`
* Verify it was saved: `# ls -la /test.mp3`
  * `$ kubectl cp oss-ns/central-v000-kjhs4:/app/status.jar -c service \Users\surendar\Downloads\test\status.jar`
  * Open the file to verify that the audio is the same as in the uploaded video.

## NEXT: Implement the "Notification" service that will consume the mp3 queue

* See "[Part 9: Notification service that reads the mp3 queue](Part_9_ Consumer_service_that_reads_the_mp3_queue.md)"

