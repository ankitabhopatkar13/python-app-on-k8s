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

*Note: kubectl client is running in context of minikube*

1. Create the namespace for the application -

`kubectl create namespace application`

2. Apply the application and service deployment yamls by running -

`kubectl apply -f app-deployment/simple-python-deployment.yml`

3. Verify that there are 3 pods running as we have given the count for replica as 3 -

`kubectl get pods -n application`

## Upgrading the application with zero downtime -

### Rolling Deployment -

In rolling deployments we will roll out the new version of application and incremently the new pods will be replacing the old pods.

1. Change the image of the deployment to point to second/new image which has new version of application.

`kubectl set image deployments/python-app python-app=python-app:1.0.2 -n application`

In a parallel window do a watch on the pods to see it creating three new pods for newer image and then terminating the older ones -

`watch kubectl get pods -n application`

By just changing the image, we didn't have to change anything in the service like the selectors or update any selectors in the deployment.

2. Check the status of the rollout by running -

`kubectl rollout status deployments/python-app -n application`

It should be successful.

3. In case if anything goes wrong, we can *rollback* by running -

`kubectl rollout undo deployments/python-app -n application`

### Blue/Green Deployment -

In blue/green deployment we first create the green environment to be available and once it's up and running we just switch the service resource to point to the application in green environment and this cycle goes on for each release.

1. Create one more file in parallel to *app-deployment/simple-python-deployment.yml* named as *app-deployment/simple-python-deployment-green.yml* . Make the following changes to it -

    a. Remove the service resource from this yaml.

    b. Change the deployment name to *python-app-green*

    c. Change template metadata label's version property to 1.0.2

    d. Change image to python-app:1.0.2

Apply the green deployment by -

`kubectl apply -f app-deployment/simple-python-deployment-green.yml`

This will create 3 more pods using the new image.

Note: The service is still pointing to the old containers.

2. Point the service to the new containers -

Change the selector version in service resource to 1.0.2 in *app-deployment/simple-python-deployment.yml*

3. Apply the service by running -

`kubectl apply -f app-deployment/simple-python-deployment.yml`

Note: We can write a script to automate these steps for blue/green deployment.

## Autoscaling

Kubernetes can scale the application by the metrics we would want to give. For ex -

To auto-scale the application when the cpu percent goes above 75 percent configure *horizontal pod autoscaler* by running -

`kubectl autoscale deployments/python-app --min=3 --max=10 --cpu-percent=75 -n application`

To delete this hpa - 

`kubectl delete hpa python-app -n application`

## Kubernetes cluster's high availabilty

Make sure to spin up a cluster which is highly available meaning -

* It's masters are spread accross atleast three different availability zones.
* The master is a cluster of three and not just a single master node.
* It's nodes are also spread accros multiple availability zones.

By ensuring above we can make sure that if any of the AZ's go down, others are available to serve the request.

Also make sure that you backup the storage volumes that have etcd hosted so that in case of cluster destruction, you can attach the volume and the data is available back.
