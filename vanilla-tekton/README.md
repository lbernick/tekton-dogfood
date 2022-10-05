A CI pipeline that responds to Github Checks "Create Check Suite" requests and posts "Create Check Run" and "Update Check Run" responses.

## Contents

- config/pipeline.yaml: a "CI" pipeline that creates a Check Run, runs tests, and finally updates the Check Run with the tests' status.
- config/github-checks-task: step 1 generates a short lived Github App Token; step 2 uses that token to call the Checks API.
- config/eventlistener.yaml and config/rbac.yaml: for responding to "Create Check Suite" events.
- jwt: a Python script for generating a JSON Web Token plus a Dockerfile to package it. Used in config/github-checks-task.
- test: Runs for testing the CI pipeline

## Steps to set up this EventListener and Pipeline
- Build the JWT image in jwt/ and push it to an image repository
  - Replace the image in the "generate-token" step of config/github-checks-task.yaml with this image
- Apply config/ contents to cluster
  - Get the external IP address of the eventlistener service
  - Create a secret named "github-secret" in the same namespace. Its data should have a key "secretToken", with some string as the value.
  This is used to secure the webhook that will be created.
  - Give the service account "container-registry-sa" permissions to pull from the container registry with the jwt image
- [Create Github App](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app)
  - Must have read and write permissions to "Checks" API
  - Must subscribe to "Check suite" and "Check run" events
  - Use the eventlistener exernal IP for the webhook address
  - Use the value of the secret created in the previous step as the webhook secret
- Install Github App on repo
  - Get app ID and installation ID and update TriggerTemplate parameters to use these values
- Allow Pipeline to authenticate as your Github App
  - Download a new private key for the app and put it in a secret named "github-app-key", for example:
  `kubectl create secret generic github-app-key --from-file=private-key.pem=<path-to-private-key>`

## Triggering the EventListener

Open a new PR on the repo the app is installed on, and push a new commit to this pull request.
This will send a "Create Check Suite" request to the EventListener webhook, triggering the PipelineRun.

## Create a Check Run locally via cURL

Generate a JSON web token:

### Run JWT script directly
```sh
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 jwt/jwt.py -p <path-to-private-key-file> -a <application-id> -i <installation-id> -c <cache-file>
```

### Run JWT script using docker
```sh
docker build jwt -t jwt
docker run -v <path-to-private-key-file>:/github-private-key jwt -p /github-private-key
```

Next, make a create check request:
```
curl -i -H "Authorization: Bearer ${JWT}" -H "Accept: application/vnd.github+json" https://api.github.com/repos/{org-or-user}/{repo-name}/check-runs -d '{"name":"ci","head_sha":"${SHA}","status":"in_progress"}'
```