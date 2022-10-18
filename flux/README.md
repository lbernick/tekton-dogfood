TODO:
- Figure out how to trigger CI when a pull request is opened or a new commit is pushed to a feature branch,
instead of when a new commit is pushed to the main branch, and how to get the git revision from the event body (if necessary)
- Figure out how to post status of PipelineRun back to Github

## Setup
- Install Tekton pipelines and triggers, enable Tekton bundles
- install flux, bootstrap w/ github
- create a webhook secret named webhook-token in the flux-system namespace: https://fluxcd.io/flux/guides/webhook-receivers/#define-a-git-repository-receiver
- get the external IP of the service and the url of the receiver
- set up github webhook on the repo with IP, URL, and webhook token