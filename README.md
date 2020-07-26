# Introduction to Kubernetes/Docker
This repo contains content for [Aramse](http://aramse.io)'s _Introduction to Kubernetes/Docker_ training.

## Prerequisites
- `git` (to clone this repo)
- `docker`
- `gcloud`

## Docker
### Build the container image
Clone this repo, navigate to the `example-apps/joker` directory, and build the container image for the joker application:
```sh
cd example-apps/joker
docker build -t my-joker-app .
```

### Run the container
Run the joker container:
```sh
docker run -p 8000:80 my-joker-app
```
Open http://localhost:8000 in your web browser.

Kill the container:
```
docker ps  # retrieve the CONTAINER-ID
docker kill <CONTAINER-ID>
```

Optionally make updates to the `serve.py` code, rebuild, and rerun the container to observe them.


## Kubernetes

### Configure access
Configure access to Google Container Registry (GCR) and the Google Kubernetes Engine (GKE) cluster we'll deploy to:
```sh
gcloud auth login   # if not already done
gcloud auth configure-docker
gcloud container clusters get-credentials k8s-intro --zone us-east1-b --project aramse-training
```

### Push the container image to GCR
Push the joker container image to GCR, replacing __<MY_NAME>__ with any value you'd like (while trying to keep it unique among participants in the training).
```sh
docker tag my-joker-app gcr.io/aramse-training/<MY_NAME>-joker-app:1.0
docker push gcr.io/aramse-training/<MY_NAME>-joker-app:1.0
```

### Install `kubectl`
```sh
gcloud components install kubectl
```

### Deploy to GKE
Edit the `k8s.yaml` file, replacing __<MY_NAME>__ with the name you chose earlier.

Deploy the joker application to Kubernetes:
```sh
kubectl apply -f k8s.yaml
```
View the `Deployment`, `Service`, and resulting `Pod` resources deployed for your joker app:
```sh
kubectl get deployments
kubectl get pods
kubectl get services
```
Open a web browser to the `EXTERNAL-IP` created for your `Service`.

Optionally you can filter to only your resources with adding a label selector `-l app=<MY_NAME>` to each of the above `kubectl` commands.

> `Namespaces`, while not covered in this training, are another k8s resource that can be used to more properly organize other resources into groups. 

### Perform a rolling update
In a separate window, run the following command to continuously request the `/hello` endpoint of your joker app:
```sh
while true; do curl <EXTERNAL-IP>/hello; echo ''; sleep 1; done
```
Update the `serve.py` file with a different return message in the `hello` request handler.

Build and push the container again (see previous section for commands), but tag it `1.1` instead of `1.0`.

Update the `k8s.yaml` file with the new `1.1` tag, and deploy it:
```sh
kubectl apply -f k8s.yaml
```
Return to the window that's continuously requesting the `/hello` endpoint and observe the responses change as the pods update.

### (Intentionally) Break the readiness probe, try another update
Cause the readiness probe to fail by editing in the handler for the readiness probe in `serve.py`, replacing the `return ''` with `return blahblah`. Also update the `hello` request handler with yet another return message.

Build and push the container again (see previous section for commands), but tag it `1.2`.

Update the `k8s.yaml` file with the new `1.2` tag, and deploy it:
```sh
kubectl apply -f k8s.yaml
```
Get the pods again:
```sh
kubectl get pods
```
Notice that you will see that the new pods do not come up as healthy, as expected, and your old pods are still running. Also going back to the window requesting `/hello` will not show your new message, only your old one. This is due to the failing readiness probe as the load balancer is smart enough to not route to any pods that are failing this probe.

Run the following to rollback to the previous version:
```sh
kubectl rollout undo deployment joker-<MY_NAME>
```

### SSH into containers
SSH into one of your joker app containers:
```sh
kubectl get pods
kubectl exec -it <POD_NAME> -- bash
```
From there, you can connect to the joker app simply using the name of its `Service`:
```sh
curl joker-<MY_NAME>
```
This is made possible with an internal DNS server that every cluster is included with, and every container within the cluster is automatically configured to point to.

You can also SSH into a new container in the same cluster, using any image:
```sh
kubectl run -it test --image centos -- bash
```

It too is automatically configured to point to the same DNS server:
```sh
curl joker-<MY_NAME>
```

### Cleanup
Delete the resources you created with the following:
```sh
kubectl delete -f k8s.yaml
```
Confirm they have been (are being) terminated:
```sh
kubectl get deployments
kubectl get pods
kubectl get services
```
