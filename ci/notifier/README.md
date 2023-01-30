This CI PipelineRun uses the experimental GitHub notifier project to create check_runs on GitHub
that display its status.

However, it has the following issues:
- The Tasks in the PipelineRun are treated as separate check runs: i.e. one "clone" check and one "tests" check
- The check runs are not created until after CI completes

## Steps to set up this EventListener and Pipeline
- Install [GitHub notifier](https://github.com/tektoncd/experimental/tree/main/notifiers/github-app) from source
- Create a new GitHub app, install it on the repository, subscribe it to pull_request events,
and set its webhook address to the eventlistener service IP.
- Generate a private key for the app and put it in a kubernetes secret.
- Edit the "github-notifier" deployment to mount the secret onto the deployment's primary container, and edit the
the GITHUB_APP_ID and GITHUB_APP_TOKEN env vars, where GITHUB_APP_TOKEN is the path to the volume mount
