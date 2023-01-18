#!/usr/bin/env bash

echo "========================================="

# Has minikube been started? 

MINIKUBE_STATUS_OUTPUT=$(minikube status)
if (exit $?) 
then
    echo "GOOD TO GO: minikube is running!"    
else
    echo "ERROR: minikube is not runnning: $MINIKUBE_STATUS_OUTPUT"

    exit 1;
fi

# Assign service directories to variables

DIR_SRC=$PWD

DIR_MYSQL=$DIR_SRC/mysql/manifests
DIR_RABBITMQ=$DIR_SRC/rabbit/manifests
DIR_MONGODB=$DIR_SRC/mongodb/manifests
DIR_AUTH=$DIR_SRC/auth/manifests
DIR_GATEWAY=$DIR_SRC/gateway/manifests
DIR_CONVERTER=$DIR_SRC/converter/manifests
DIR_NOTIFICATION=$DIR_SRC/notification/manifests

# Start each service using "kubectl apply ./":
echo;
cd "$DIR_MYSQL"; kubectl apply -f ./;
cd "$DIR_RABBITMQ"; kubectl apply -f ./;
cd "$DIR_MONGODB"; kubectl apply -f ./;
cd "$DIR_AUTH"; kubectl apply -f ./;
cd "$DIR_GATEWAY"; kubectl apply -f ./;
cd "$DIR_CONVERTER"; kubectl apply -f ./;
cd "$DIR_NOTIFICATION"; kubectl apply -f ./;

# Print the status of our minikube pods

KUBECTL_GET_PODS_OUTPUT=$(kubectl get pods -o wide);
echo;
echo "Status of our Kubernetes pods after STARTING services:"
echo;
echo "$KUBECTL_GET_PODS_OUTPUT";    
echo;
echo "========================================="

