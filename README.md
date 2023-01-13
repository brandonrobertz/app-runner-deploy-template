# App Runner GitHub Deploy Template

Hello! This is a template that builds and re-deploys web applications based on GitHub Action runs to [AWS App Runner][app-runner].

## Setup

Make a new repo, using this as a template.

## Step 1: Add GitHub Action Secrets

Go to the GitHub Action secrets menu by going to `Settings` -> `Secrets and variables` -> `Actions`. Add the following repository secrets:

- `AWS_ACCESS_KEY_ID`: User ID that has permission to deploy to App Runner
- `AWS_SECRET_ACCESS_KEY`: Secret key corresponding to the above user
- `AWS_REGION`: Region, needs to be same as the GitHub connection within App Runner
- `AWS_APP_RUNNER_SERVICE_NAME`: Name of the App Runner service to create/update. Make sure this isn't already used if you're creating a new app.
- `AWS_CONNECTION_SOURCE_ARN`: ARN of the App Runner GitHub connection (there should be one already present in AWS)

## Step 2: Complete the deploy settings

Make sure you choose the appropriate runtime (Python, Node, etc), CPU, RAM and other settings in the action configuration: `.github/workflows/deploy.yml`

## Step 3: Run the action

This is set up to primarily deploy by pushing a release to the repo. Or you can manually run it by going to: `Actions` -> `Deploy to App Runner` (in right menu) -> `Run workflow` (button) -> `Run workflow`.
