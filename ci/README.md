This repo contains configuration to set up an end-to-end Github-based CI pipeline with Tekton.

Contents:
- vanilla_tekton: a Github CI workflow using only Tekton Pipelines and Tekton Triggers.
- notifier: the same workflow using the experimental [GitHub App notifier](https://github.com/tektoncd/experimental/tree/main/notifiers/github-app)
- flux: the same workflow using Flux for events and notifications, plus Tekton Triggers and Tekton Pipelines