# Explaining Kubernetes & it's configuration (manifest files)

* NOTE: Starts at 1:19:20 in the [lecture video](https://www.youtube.com/watch?v=hmkF77F9TLw).

## What is Kubernetes?

* Eliminates manual steps needed to deploy & scale containerized apps.
* Monitors pods. Restarts if one fails.
* Takes care of scaling pods up/down.
  * `$ kubectl scale deployment --replicas=6 service`
  * Will configure the load balancer to include any new pods. Or exclude if down-scaling.
* Kubernetes Objects: Persisted entitites in the Kubernetes system.
  * Object: A "record of intent": Kubernetes will try to fullfill the requirement.
  * Specifies the cluster's desired state.
* The Kubernetes "Control Plane" actively manages evary Object's STATE to match the "desired state" you supply.
  * => Compares the "Current State" with the "Intended State" (Desired State).
* Use the "Kubernetes API" to communicate the Object's "Desired State" to the Control Plane
  * => Use the `$ kubectl` command. 
  * Note: Use `$ kubectl config` to interact with a remote server.

## Explaining the yaml config files

* NOTE: Starts at 1:24:20 in the [lecture video](https://www.youtube.com/watch?v=hmkF77F9TLw).

* CONCEPTS:
  * See the [Kubernetes API reference](https://kubernetes.io/docs/reference/).
  * Press [Workload Resource](https://kubernetes.io/docs/concepts/workloads/controllers/).
    * NOTE: Workloads resources are responsible for managing and running your containers on the cluster.
      * Containers are created by Controllers through Pods.
      * Pods run Containers and provide environmental dependencies such as shared or persistent storage Volumes and Configuration or Secret data injected into the container.
  * Press [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

* Required fields:
  * apiVersion :Kubernetes API version
  * kind: type of Object we want to create
  * metadata: Uniquely idetifies the Object
  * spec: The desired STATE of the Object. E.g. the "Deployment Spec".
    * See the [Kubernetes API reference](https://kubernetes.io/docs/reference/).
    * Press [Deployments](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#deployment-v1-apps).
    * Press [DeploymentSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#deploymentspec-v1-apps).
* About "spec:" section of a "Deployment" Object.
  * "selector" and "template" (1:27:40 i video):
    * The labels in these 2 sections must match 
    * => Pods are "labelled" using key-value-pairs, e.g. "app: auth".
  * "strategy": How to replace existing pods with new ones.
    * "maxSurge": 1:30:30 in video.
  * "template": Describes the Pods that will be created.
  * "spec: spec: ": This is the "Pod" spec, not the "Deployment" spec.
    * Define "container", set the "image" to use, ports (EXPOSE in Docker):
      * INFORMATIONAL (serves as doc): If not specified => Port will still be exposed.
  * "envFrom": video at 1:33:30: configMapRef & secretRef.
    * These are both separate Kubernetes Objects ("kind" and "name" in a separate yaml file).

## NEXT: Gateway service

* See: [The "Gateway service"](docs/PART_5_Gatway_service.md)