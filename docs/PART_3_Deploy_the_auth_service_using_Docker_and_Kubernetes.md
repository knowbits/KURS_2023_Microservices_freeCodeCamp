# Deploy the auth service (Python) using Docker and Kubernetes

* Video: 52:40. <https://www.youtube.com/watch?v=hmkF77F9TLw>

* Steps:
  * Create Docker image for the "Auth" service, push it to a repository.
  * Kubernetes config will pull the Docker image from the repo.
  * Create deployments within our local Kubernetes cluster.

## Activate our "Python virtual environment" named "venv"

* `$ source ./venv/bin/activate`
* Verify it: 
  * `$ env | grep VIRTUAL`

## FUTURE: Create and Use a "virtual environment" with one of these approaches instead:

1. Use "Pipenv"

   * Basic usage: <https://pipenv.pypa.io/en/latest/basics>
   * Article: [How to manage your python virtualenvs with Pipenv](https://medium.com/test-automation-university/how-to-manage-your-python-virtualenvs-with-pipenv-f1220ded702e)

2. "Conda" (maybe)
   * Article: [Using a Virtual Environment to Avoid Seeming like a Sadist](https://boscacci.medium.com/why-and-how-to-make-a-requirements-txt-f329c685181e) (Why and How to make a Requirements)
     * Uses "Conda" to switch between "Python virual environments".

* Using "requirements.txt" is obsolete!
  * => The modern way is to use "[Pipenv](https://pipenv.pypa.io/en/latest/basics)".
  * It creates the "Pipfile": with all installed dependencies.
  * "Pipfile" should be saved in "git".

## Create a Docker image for the "auth" service

* Create "src/auth/Dockerfile".
* Find the version of Python: `$ python3 --version`  # => Python 3.10.7

## PROBLEM detected: "requirements.txt" contains all installed Python packages on the system

* The following DID NOT WORK well:
  * Create the "python dependencies" file, run: `$ pip freeze > requirements.txt`
  * => PROBLEM: Includes all Python packages installed on the system!!

* "pipreqs" - a "quick fix"
  * A better approach is to instead use "pipreqs" to generate "requirements.txt" 
  * https://github.com/bndr/pipreqs
  * "Generate pip requirements.txt file based on imports of any project."
  * Run: `$ pipreqs .`

* SOLUTION: Decided to use "Pipenv" for managing Python package dependencies  
  * See "[Setup, config and use of "Pipenv"](PART_2c_Python__Pipenv_and_Pipfile_for_dependencies.md)".

* "Pipenv" and "Pipfile": Python dependencies
  * NOTE: A more modern approach for DEPENDENCIES seems to be to use "Pipenv" instead of "requirements.txt".
  * "Pipenv" creates "Pipfile": contains all Python dependencies.
  * The (old) "requirements.txt" can be created from "Pipfile".

* FUTURE: Using "Pipenv" with Docker is described here:
  * <https://pipenv.pypa.io/en/latest/basics/#pipenv-and-docker-containers>

## How to make "minikube" use local Docker images

* NOTE: The lecture (at 1t 2min) uses "Docker Hub" to push and pull images.
  * https://www.youtube.com/watch?v=hmkF77F9TLw
  * => We choose to use LOCAL IMAGES instead: 
  * See description in [How to use local Docker images with Minikube (Kubernetes)](PART_3b_HOW_TO_Use_local_Docker_images_with_minikube.md)

## COMMANDS: Use a local Docker image with "minikube"

1. In the Kubernetes "Deployment file", after the line ` image: sweasytech/auth` add line: `imagePullPolicy: Never`
   * => This will prevent Kubernetes from downloading from a remote image repository.
2. `$ minikube start`
3. `$ minikube image build -t my-image/0.0.1 .`
    * => The image will be instantly available to Minikube.
4. `$  minikube image ls`  => List all images in minikube.
5. `$ kubectl run my_pod_1 --image=my-image:0.0.1`
    * Add `--image-pull-policy=Never` if "imagePullPolicy: Never" is not specified in the Kubernetes manifest.
6. `$ kubectl get pods`
    * => Is the image up and running in minikube?
7. `$ kubectl delete pod my_pod_1`

### Alternative 1: Download a Docker image and use it in minikube, do:

0. Replace "Step 3)" above with:
1. `$ eval $(minikube docker-env)`
   * => Points the "local Docker daemon" to the "minikube internal Docker registry".
2. `$ docker pull hello-world`

### Alternative 2: Load a "local Docker image" directly into minikube

0. Replace "Step 3)" above with:
1. `$ docker pull hello-world`
2. `$ minikube image load hello-world`

## Typical sequence of commands: docker, kubectl, minikube

```bash
 # NEEDED? Requires stop + delete after (of minikube).
minikube config set driver docker
minikube start

minikube ip   # IP address of minikube
kubectl cluster-info  # => IP of 1) Control plane, 2) CoreDNS.
kubectl get nodes # Shows only "Control plane" node after minikube startup.

kubectl config get-contexts # Get the list of confogrued contexts. With "namespaces".
kubectl config use-context minikube # Set the context of "kubectl" to "minikube".

# ALternative 1: Build image locally with minikube: 
minikube image build -t my-image/v1 .

# Alternative 2: Pull an image from a remote repo: 
docker pull hello-world
minikube image load hello-world

# List all images available in minikube
minikube image ls

kubectl run my-pod --image=my-image:v1 
kubectl run hello-world-pod --image=hello-world --image-pull-policy=Never
# OPTION (kubectl):
#   --image-pull-policy=Never : Not needed if "imagePullPolicy: Never" is used in the Kubernetes manifest file (.yaml).

kubectl get po -A   # -A: Pods in "ALL NAMESPACES": Including "system" related pods.
kubectl get pods

kubectl delete pod hello-world-pod
minikube image rm my-image/v1
```

## Create the Kubernetes manifest for the "Auth" service (Python)

* NOTE: From the [lecture video](https://www.youtube.com/watch?v=hmkF77F9TLw) at 1:07:00.
* `$ mkdir manifests; cd manifests`  # In "src/auth/" folder.
* `$ touch auth-deploy.yaml configmap.yaml secret.yaml service.yaml`
* Copy contents from the corresponding repo files "
  * [auth-deploy.yaml](https://github.com/selikapro/microservices-python/blob/main/src/auth/manifests/auth-deploy.yaml)
  * [configmap.yaml](https://github.com/selikapro/microservices-python/blob/main/src/auth/manifests/configmap.yaml)
  * [secret.yaml](https://github.com/selikapro/microservices-python/blob/main/src/auth/manifests/secret.yaml)
  * [service.yaml](https://github.com/selikapro/microservices-python/blob/main/src/auth/manifests/service.yaml)
* Check the status of the cluster with "k9s": `$ k9s` (CTRL+C: Quit, 0: All)
* Build the "auth" Docker image, run `cd ..; minikube image build -t auth .`
* Verify that the "auth" image is now in the "minikube internal Docker registry": `$ minikube image ls`
  * => Will list: `docker.io/library/auth:latest`
* Change "auth-deploy.yaml":
  * Replace line "image: sweasytech/auth" with "image: auth".
  * Add this line after: "imagePullPolicy: Never"
    * Prevents Kubernetes from downloading images from an external repo.
* Deploy the "auth" service to Kubernetes, run: `$ cd mainfests; kubectl apply -f ./`
* Check the logs: 1) RUn `$ k9s` | Open one of the pods (ENTER) | Open the "container" (ENTER) 
  * => Says "Waiting for logs..." => Trick is to press "0".
* To open a "Shell" within the container: Press "Enter" on the Pod, then press "s" (Shell) on the "container".
  * Run `$ env` to theck that all the "MYSQL_*" "Environment variables" from "configmap.yaml" have been set.
  * Or run `$ env | grep MYSQL`

## Explaining the Kubernetes & configuration

* See * [Explaining Kubernetes and it's configuration (manifests)](PART_4_Explaining_Kubernetes_and_config_files.md)
