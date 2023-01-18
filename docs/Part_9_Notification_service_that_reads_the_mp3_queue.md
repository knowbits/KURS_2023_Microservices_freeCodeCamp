# Notification service that reads the mp3 queue (a "consumer" service)

* See video at "4:18:00".

## Update `gateway/server.py`

* See video at "4:20:00".

## Create the "Notification" service

* See video at "4:29:30".
* Create `consumer.py` and `send/email.py`
* Create a Python virtual environment: SEE how its done in EARLIER services.

## Create `Dockerfile` and build it

* See video at "4:41:15".
* Create the `Dockerfile`.
* Build the Docker image directly into the "minikube image registry":
  * `$ minikube image build -t notification .`

## Create the Kubernetes manifest files

* See video at "4:41:45".
* Create the Kubernetes "manifests" directory and files.
* Edit `notification-deploy.yaml`
  * Change line `replicas: 4` to `replicas: 1`, for easier debugging.
  * Change line `image: sweasytech/notification` to `image: notification`
    * Will use the image residing in the "minikube image registry".
  * Add this line after the `image: notification` line:
    * `imagePullPolicy: Never`

## Create a dummy Gmail account

* Create the account here: <https://accounts.google.com/signup/v2/webcreateaccount>
* ACCOUNT info:
  * USER: broedsmuler@gmail.com
  * PWD: pinchme2times
* SET UP ""Less secure app access" for Gmail:
  * Press the account picture (upper right).
  * Choose "Manage your Google account"
  * Choose "Security" in the left side menu/list.
  * Choose "Less secure app access".
    * PROBLEM: NOT AVAILABLE ANYMORE. 
    * REASON: "As of May 30 2022 google has removed the less secure apps option"
* => SOLUTION: See "[Sign in with App Passwords](https://support.google.com/mail/answer/185833?hl=en)"
  * Open your "Google Account": <https://myaccount.google.com/>
  * Select "Security": <https://myaccount.google.com/security>
  * Enable "2-step Verification": <https://myaccount.google.com/signinoptions/two-step-verification>
  * Under "Signing in to Google," select "App passwords":
    * <https://myaccount.google.com/apppasswords>
    * Choose "Mail" as the application.
    * For "Device:" select "Other". Name it "MICROSERVICES_COURSE"
    * Generates an "app password", e.g. `bpurthcofufdmluz`
    * Message: _"Replace your password with the 16-character password shown above. Just like your normal password, this app password grants complete access to your Google Account."_
* In the file `notification/manifests/secret.yaml`, make these changes:
  * `GMAIL_ADDRESS: "broedsmuler@gmail.com"`
  * `GMAIL_PASSWORD: "bpurthcofufdmluz"` (the "app password")

## Change the email in the "user" table of the MySQL database

* See video at "4:45:20"
* Run `$ kubectl exec service/mysql -it -- /bin/bash`
* Run these "mysql" commands:
  * `use auth;`, `show tables;`, `select * from user;`
* Change the email of the user: 
  * `UPDATE user SET email = 'broedsmuler@gmail.com'`
  * NOTE: Password is still `Admin123`
* NOTE: If running "mysql" as a Pod, then also change this line in `mysql/manifests/pod.yaml`:
  * `INSERT INTO user (email, password) VALUES ('broedsmuler@gmail.com', 'Admin123');`  

## Get a JWT for the changed user (new email address)

* `$ minikube tunnel`
* `$  sudo curl -X  POST http://mp3converter.com/login -u broedsmuler@gmail.com:Admin123`
  * => Will return a new JWT.
    * NOTE: Don't include the last sign: a `%`.

## Upload a video file again using `curl`

* Make sure the new "notification" service has been started.
* `$ curl -X POST -F 'file=@video_file.mp4' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJyb2Vkc211bGVyQGdtYWlsLmNvbSIsImV4cCI6MTY3NDExNjQ4MCwiaWF0IjoxNjc0MDMwMDgwLCJhZG1pbiI6dHJ1ZX0.sTfT3elfD9xCbcVUuRuL2QHosYaVuUn2g2Ra3iQDYTw' http://mp3converter.com/upload`
  * NOTE: Assumes that ``video_file.mp4` is available in the current directory.
* If ERROR: => Try these steps:
  * 1. Restart the "gateway service".
  * 2. Check RabbitMQ and verify that the two queues have been created: "mp3s" and "videos".

## Check the email in Gmail and download the mp3 using `curl`

* See video at "4:58:40". 
* Log in to Gmail and verify that the "notification" service has sent an email.
  * Subject: "MP3 Download"
* Copy the "mp3 file_id" from the email body, typically something like "63c7ae094f5d7e6ee2bb858c".
* Download the mp3 file by riunning: 
  * `$ curl --output mp3_downloaded.mp3 -X GET -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJyb2Vkc211bGVyQGdtYWlsLmNvbSIsImV4cCI6MTY3NDExNjQ4MCwiaWF0IjoxNjc0MDMwMDgwLCJhZG1pbiI6dHJ1ZX0.sTfT3elfD9xCbcVUuRuL2QHosYaVuUn2g2Ra3iQDYTw' "http://mp3converter.com/download?fid=63c7ae094f5d7e6ee2bb858c"`
  * NOTE: We use the "file_id" in the GET request to the "/download" route.
* Your should now have the file `mp3_downloaded.mp3` in your CWD (current working directory).

## And that's it!

* THE END.
