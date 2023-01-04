This repo contains configuration to set up end-to-end CI and CD pipelines with Tekton.

Contents:
- CI: a Github CI workflow integrated with Github Checks
- CD: a Github CD workflow that builds and pushes an image from a repository when there is a
change pushed to the main branch

TODO:
- A workflow that polls a Git repository for changes at a regular cadence
