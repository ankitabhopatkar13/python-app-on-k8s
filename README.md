# python-app-on-k8s
## kubernetes cluster setup on AWS EKS -

1. Manually created a cluster by specifying 3 subnets in different availability zones to make sure of high availability
2. Once the cluster was created, set kubectl context to EKS Cluster following https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
   
   **Note** : To set the config and use EKS, use the cli credentials of the only user that you used when clicking on create cluster from console.
3. Create nodes and configure to the cluster by following the document - https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html

## Python App Docker Build - 

1. After cloning the repo build docker image by -

`docker build . -t python-app:1.0.1`

2. Run the application by running -

`docker run -it -p 5000:5000 python-app:1.0.1`

Access the application at -

`http://localhost:5000/version`

