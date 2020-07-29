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

View the built container image:
```sh
docker images
```

### Run the container
Run the joker container:
```sh
docker run -p 8000:80 my-joker-app
```
Open http://localhost:8000 in your web browser.

### View info on the container
In a separate window, run the following to inspect the container's properties:
```sh
docker ps  # retrieve the CONTAINER-ID
docker inspect <CONTAINER-ID>
```

### Cleanup
Kill the running container:
```
docker ps  # retrieve the CONTAINER-ID
docker kill <CONTAINER-ID>
```

Optionally make updates to the `serve.py` code, rebuild, and rerun the container to observe them.


## Kubernetes

### Configure access
Configure access to Google Container Registry (GCR) and the Google Kubernetes Engine (GKE) cluster we'll deploy to, and install `kubectl`:
```sh
gcloud auth login   # if not already done
gcloud auth configure-docker
gcloud components install kubectl
gcloud container clusters get-credentials k8s-intro --zone us-east1-b --project aramse-training
```

### Push the container image to GCR
Push the joker container image to GCR, replacing __<MY_NAME>__ with any value you'd like (while trying to keep it unique among participants in the training).
```sh
docker tag my-joker-app gcr.io/aramse-training/<MY_NAME>-joker-app:1.0
docker push gcr.io/aramse-training/<MY_NAME>-joker-app:1.0
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
Notice that you will see that the new pods do not come up as healthy, as expected, and your old pods are still running. This is due to the failing readiness probes as Kubernetes will only terminate older pods if new ones are deployed that are passing readiness probes.

Also going back to the window requesting `/hello` will not show your new message, only your old one. This is also due to the failing readiness probe as the `Service` is smart enough to not route to any pods that are failing this probe.

Run the following to rollback to the previous version:
```sh
kubectl rollout undo deployment joker-<MY_NAME>
```

### View container logs
```sh
kubectl get pods  # retrieve POD_NAME
kubectl logs <POD_NAME> -f
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
This is made possible with an internal DNS server that every cluster includes, and which every container within the cluster automatically uses.

You can also SSH into a new container in the same cluster, using any image:
```sh
kubectl run -it test --image centos <MY_NAME> -- bash
```

It is also configured to use the same DNS server:
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
