# python-app-on-k8s
## Kubernetes cluster setup on Minikube -

Install Minikube using brew (you need VirtualBox installed)

`brew cask install minikube`

`minikube start --memory 6000 --cpus=4 (open VirtualBox and see minikube  instance running, first time it can take upto 10-15 min)`

## Install Kubernetes command line -
`brew install kubectl`

## For using docker daemon running on minikube run the following -
`eval $(minikube docker-env)`

## Python App Docker Build - 

Make sure to be in the context of minikube docker daemon (`eval $(minikube docker-env)`).

### Docker image having version 1.0.1

1. After cloning the repo build docker image by -

`docker build . -t python-app:1.0.1`

2. Run the application by running -

`docker run -it -p 5000:5000 python-app:1.0.1`

Access the application at -

`http://localhost:5000/version`

### Docker image having version 1.0.2

1. Change the version in python-app-on-k8s/python-app/src/VERSION.txt to 1.0.2 and run -

`docker build . -t python-app:1.0.2`

2. Run the application by running -

`docker run -it -p 5000:5000 python-app:1.0.2`

Access the application at -

`http://localhost:5000/version`

You can see the version changed in this image.

## Deploying application on Kubernetes cluster

1. Create the namespace for the application -

`kubectl create namespace application`

2. Apply the application and service deployment yamls by running -

`kubectl apply -f app-deployment/simple-python-deployment.yml`

3. Verify that there are 3 pods running as we have given the count for replica as 3 -
`kubectl get pods -n application`

## Upgrading the application with zero downtime -

### Rolling Deployment -

1. Change the image of the deployment to point to second/new image.

`kubectl set image deployments/python-app python-app=python-app:1.0.2 -n application`

In a parallel window do a watch on the pods to see it creating three new pods for newer image and then terminating the older ones -

`watch kubectl get pods -n application`

By just changing the image, we didn't have to change anything in the service like the selectors or update any selectors in the deployment.

2. Check the status of the rollout by running -

`kubectl rollout status deployments/python-app -n application`

It should be successful.

3. In case if anything goes wrong, we can *rollback* by running -

`kubectl rollout undo deployments/python-app -n application`

