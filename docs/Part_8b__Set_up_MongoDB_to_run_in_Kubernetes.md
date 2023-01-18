# Set up MongoDB to run in Kubernetes

## How to access a running "mongodb" Pod

## Download the mp3 file from "mongodb" to verify the audio

* Forward the port of the "mongodb" pod:
  * Get the POD NAME: `$ kubectl get pods`
  * Get the port: `$  kubectl get pod mongo-869f6488c8-vk9rj --template='{{(index (index .spec.containers 0).ports 0).containerPort}}{{"\n"}}'`
  * Forward the Pod's port: `$ kubectl port-forward mongo-869f6488c8-vk9rj 27017:27017`

* Access the "mongodb" Pod using the `mongosh` tool
  * `$ mongosh` or `$ mongosh "mongodb://127.0.0.1:27017"`

* Use the `mongofiles` tool to get a file with a gven ObjectId and save to a local file (./test.mp3):
  * `$ mongofiles --db=mp3s get_id --local=test.mp3 '{"$oid": "63c47dc3e2a97d508f7e75b9"}'`
* Verify that the file was saved: `# ls -la test.mp3`

## Kubernetes manifest files for a "mongodb" service

* NOTE: Uses the official "MongoDB Management" image.
  
* Based on these instructions: "[Deploy your first Flask+MongoDB app on Kubernetes](https://levelup.gitconnected.com/deploy-your-first-flask-mongodb-app-on-kubernetes-8f5a33fa43b4)"

* Create the folder for the Deployment: `$ mkdir src/mongodb/manifests`

* Create the 4 yaml files for the service, see below.
* Start mongodb: `$ kubectl apply -f ./`

* Once mongodb is running, use the `mongosh` tool to interact with mongodb:
  * `$ kubectl exec service/mongo -it -- /bin/bash`
  * Then run `# mongosh` in the container shell.

* Also, refer to `mongo` instead of `host.minikube.internal` in `gateway/server.py`, so that the 2 code lines become:
  * `mongo_videos = PyMongo(server, uri="mongodb://mongo:27017/videos")`
  * `mongo_mp3s = PyMongo(server, uri="mongodb://mongo:27017/mp3s")`

* Finally, change the line in `converter/consumer.py` to:
  * `dbclient = MongoClient("mongo", 27017)`

Here are the 4 yaml files (from the [article](https://levelup.gitconnected.com/deploy-your-first-flask-mongodb-app-on-kubernetes-8f5a33fa43b4)):

1: "mongo-service.yaml"

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongo
spec:
  selector:
    app: mongo
  ports:
    - port: 27017
      targetPort: 27017
```

2: "mongo-deployment.yaml"

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo
spec:
  selector:
    matchLabels:
      app: mongo
  template:
    metadata:
      labels:
        app: mongo
    spec:
      containers:
        - name: mongo
          image: mongo
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: storage
              mountPath: /data/db
      volumes:
        - name: storage
          persistentVolumeClaim:
            claimName: mongo-pvc
```



3: "mongo-pv.yaml"

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mongo-pv
spec:
  capacity:
    storage: 256Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/db
```

4: "mongo-pvc.yaml"

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongo-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 256Mi
```

