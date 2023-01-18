# How to use local Docker images with Minikube (Kubernetes)

## 4 METHODS of making "minikube" use local Docker images

* NOTE: The lecture (1t 2min) uses "Docker Hub" to push and pull images.
  * https://www.youtube.com/watch?v=hmkF77F9TLw
  * => We choose to use LOCAL IMAGES instead.

1. Point the "local Docker deamon" to minikube's internal Docker registry:
   * See article "[How to Run Locally Built Docker Images in Kubernetes](https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d)".
   * The `$ minikube docker-env` command outputs the "environment variables" needed to point the "local Docker daemon" to the "minikube internal Docker registry"
   * To apply these variables to the current shell run: `eval $(minikube docker-env)`
     * OR? : `$ eval $(minikube -p minikube docker-env)`

2. Push your local Docker image directly to minikube:
   * `$ minikube image load [image name]`
   * NOTE: Saves time from building the images in minikube again.
   * See article "[Two easy ways to use local Docker images in Minikube](https://levelup.gitconnected.com/two-easy-ways-to-use-local-docker-images-in-minikube-cd4dcb1a5379)".

3. EASIEST? Build a Docker image "inside" minikube:
   * `$ minikube image build -t  [image name] .`
     * Example: `$ minikube image build -t my-image/v1 .`
   * => Using the minikube `$ image build` command the image is instantly available to Minikube 
     * It doesn't have to be explicitly loaded in a second step via the minikube `$ minikube image load` command.
   * See article "[Two easy ways to use local Docker images in Minikube](https://levelup.gitconnected.com/two-easy-ways-to-use-local-docker-images-in-minikube-cd4dcb1a5379)".
  
4. Run a local "Docker Registry" server (a bit involved)
   * Official: [Deploy a registry server](https://docs.docker.com/registry/deploying)
   * Also described [here](https://stackoverflow.com/questions/67028514/how-to-locally-backup-the-images-of-a-local-docker-registry/67030771#67030771) or [here](https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube)

5. Run the "Docker Registry" as a service in "systemd"
   * Misc descriptions on www.. Quite involved..
   * [How to Configure Private Registry for Kubernetes cluster running with containerd](https://mrzik.medium.com/how-to-configure-private-registry-for-kubernetes-cluster-running-with-containerd-cf74697fa382)
  

## METHOD 2: Configure "minikube" to use local Docker images
  
* => We make "minikube" to use local Docker images as described [here](https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube).

```bash
# Start minikube
minikube start

# To create the image registry on minikube's Docker:
# => Set "docker env".
# 
# Must be set in EVERY new terminal!
#   NB! Must also be run BEFORE rebuilding images!
#
eval $(minikube docker-env)

# ALT. 1: Get existing image from online repo:
docker pull hello-world

# ALT. 2: Build image locally
docker build -t foo:0.0.1 .

# Run a local "Docker image" in minikube
#
# NB! Must set "image-pull-policy=Never" to prevent from downloading image.
#     OR: Add "imagePullPolicy: Never" in the Kubernetes "Deployment" mainfest file.
# 
# NOTE: The following will give STATUS=CrashLoopBackOff when running "$ kubectl get pods"
kubectl run my-hello-world --image=hello-world --image-pull-policy=Never

# Check that it's running
kubectl get pods
```
