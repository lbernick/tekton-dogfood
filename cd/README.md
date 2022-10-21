This repo contains configuration to set up an end-to-end Github-based CD pipeline with Tekton.
The Pipeline builds the contents of a repo and pushes the image to Google Artifact Repository.
It's triggered when a change is pushed to the main branch of the repo.

Contents:
- vanilla_tekton: implementation using Tekton Triggers and Pipelines
TODO: implementation using Tekton workflows
