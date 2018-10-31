# python-app-on-k8s
## kubernetes cluster setup on Minikube -

Install Minikube using brew (you need VirtualBox installed)

`brew cask install minikube`

`minikube start --memory 6000 --cpus=4 (open VirtualBox and see minikube  instance running, first time it can take upto 10-15 min)`

## Install Kubernetes command line -
`brew install kubectl`

## For using docker daemon running on minikube run the following -
`eval $(minikube docker-env)`

## Python App Docker Build - 

1. After cloning the repo build docker image by -

`docker build . -t python-app:1.0.1`

2. Run the application by running -

`docker run -it -p 5000:5000 python-app:1.0.1`

Access the application at -

`http://localhost:5000/version`

