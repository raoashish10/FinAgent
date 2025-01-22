## Instructions

1. Install minikube
`brew install minikube`
2. Start minikube
`minikube start`
3. Create pod for postgres using postgres-deployment.yaml, creates it using docker registry 
`kubectl apply -f postgres-deployment.yaml`
4. Need to build finagent API's image in minikube's docker because it is not publically available on the docker registry 
    a. Configure docker commands to run in minikube's docker environment for the current session.
        `eval $(minikube docker-env)`
    b. Build docker image from root directory
        `docker build -t finagent:latest .`
5. SSH into minikube's docker image using
    `minikube ssh`
    
    Check for list of docker images to ensure we have both postgres and finagent
    `docker images`
6. If docker image found in above command, exit from minikube docker container and create the API pod 

`kubectl apply -f fastapi-deployment.yaml`

7. Check status of pods, they should be RUNNING

`kubectl get pods`

8. To access the API, forward your system's localhost:8000 to connect to localhost:80 of the pod.

`kubectl port-forward pod/fastapi-584c7876f5-6w4w9 8000:80`
- Replace fastapi's pod name with the one you see when you run `kubectl get pods`
- Portforwarding 8000:80 because fastapi is hosted on port 80, as mentioned in the Dockerfile for fastapi. 

Extras:

1. To see logs of a pod:

`kubectl logs <pod-name>`

2. To update an image in a deployment,
    
    a. First build the image
    
    b. Then set the latest image for the deployment

    `kubectl set image deployment/fastapi finagent=finagent:latest`

    c. Restart rollout in deployment for pods

    `kubectl rollout restart deployment/<deployment-name>`

3. Connection string for postgres db changes when using k8s

`DB_URI="postgresql://postgres:password@postgres-service:5432/finagent?sslmode=disable"` 
