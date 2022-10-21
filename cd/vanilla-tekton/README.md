This example is meant to run on a GKE cluster with Workload Identity enabled.
Steps to use this example:
- Install Tekton Pipelines with alpha features and Tekton Triggers.
- Create a secret named "github-secret", with a key called "secretToken".
This secret will be used to set up the webhook.
Example:
```
echo -n "abc123" > super-secret.txt
kubectl create secret generic github-secret --from-file=secretToken=super-secret.txt
```
- Create a Github webhook on your repo
  - Subscribe to push events
  - Choose content type application/json
  - Set its webhook URL to the external IP of the eventlistener ingress (e.g. "http://<ip-addr>:8080")
  - Set its secret to the secret created in the first step
- Create a Google Service account named "builder" with permissions to push to Artifact Registry.
```sh
gcloud iam service-accounts create builder
gcloud projects add-iam-policy-binding <project> --member="serviceAccount:builder@<project>.iam.gserviceaccount.com" --role roles/artifactregistry.writer
```
- [Enable a webhook](https://developers.google.com/chat/how-tos/webhooks) on the Google chat space.
- Create a Google Service account named "notifier" with permissions to post to Google chat.
```sh
gcloud iam service-accounts create notifier
gcloud projects add-iam-policy-binding <project> --member="serviceAccount:<project>.svc.id.goog[default/notifier]" --role roles/chat.owner
```
