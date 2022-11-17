This repo contains configuration to set up an end-to-end Github-based CI pipeline with Tekton.

Contents:
- vanilla_tekton: a Github CI workflow using only Tekton Pipelines and Tekton Triggers.
- workflows (TODO): the same workflow using [Tekton Workflows](https://github.com/tektoncd/experimental/tree/main/workflows)
- flux: the same workflow using Flux for events and notifications, plus Tekton Triggers and Tekton Pipelines