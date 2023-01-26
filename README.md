# App Runner GitHub Deploy Template

Hello! This is a template that builds and re-deploys web applications based on GitHub Action runs to [AWS App Runner][app-runner].

There's a fully functional example of this workflow in the [pixel-dashboard repository][pixel-dashboard].

## Setup Instructions

### Step 1: New repo

Make a new repo, using the [app-runner-deploy-template][app-runner-deploy-template] template.

### Step 2: Add GitHub Action Secrets

Go to the GitHub Action secrets menu by going to `Settings` -> `Secrets and variables` -> `Actions`. Add the following repository secrets:

- `AWS_ACCESS_KEY_ID`: User ID that has permission to deploy to App Runner. Attach any policies to this user that the application needs to perform its tasks. If you're creating a new user you can follow the instructions below about minimum permissions.
- `AWS_SECRET_ACCESS_KEY`: Secret key corresponding to the above user.
- `AWS_REGION`: Region, needs to be same as the GitHub connection within App Runner. The application will be deployed into this region.
- `AWS_APP_RUNNER_SERVICE_NAME`: Name of the App Runner service to create/update. Make sure this isn't already used if you're creating a new app.
- `AWS_CONNECTION_SOURCE_ARN`: ARN of the App Runner GitHub connection. There should be [one already present in AWS][gh-integrations-console]. The proper ARN will have the following format: `arn:aws:apprunner:<<region>>:<<account-id>>:connection/apprunner-githubaction-connect/<<hash>>`

### Step 3: Complete the deploy settings

You need to set up the App Runner environment by editing the configuration file: `.github/workflows/deploy.yml`

By default, the environment is Python3, with dependencies in `requirements.txt` and basic unit tests in the `tests/` folder (using Python's builtin `unittest` library). If you need anything more advanced, change the `build-command` and `start-command` settings in the GitHub Action.

If you're not using a Python3 environment, you can choose from one of the following:

`PYTHON_3 | NODEJS_12 | NODEJS_14 | CORRETTO_8 | CORRETTO_11`

CPU, RAM and other settings are also available there.

#### Environment Variables

If you need to pass any environment variables from the GitHub Action into the App Runner config, you can add them in your Action Secrets and then add them to the `copy-env-vars` list. Some necessary enviroment variables have already been added for you (IAM credentials and region).

### Step 4: Run the action

Running this action will deploy the app. If it doesn't exist, it will be created.

You should see the App Runner service in the AWS console now if all went well. If there was a failure, the workflow run will have logs detailing the problem.

### Step 5: Deployments

Pushing to the `main` branch will deploy this to App Runner. You don't need to run the GitHub Action to deploy, App Runner is listening for commits to `main`. *Use feature branches while developing.* App Runner will automatically roll back any commits that cause a build error or a failed health check.

You can change App Runner settings by doing the following:

1. Go to the [AWS App Runner Console](https://us-east-1.console.aws.amazon.com/apprunner/home?region=us-east-1#/services)
2. Click on the appropriate service
3. Go to the `Configuration` tab
4. In the section you want to change, click the `Edit` button.

A project tag could be a good idea, if there are other non-App Runner resources associated with this service.

## Misc Notes

### Tip: Get your basic deploy working before you complicate it

There's no easy way to see why your build and start commands are failing. App Runner simply says that the deploy failed and tries to roll back. If you want logs out of this we would need to set up a whole ECR stack and CloudWatch.

My advice is to get a skeleton of you app working and then get your environment all set up and push things up piece by piece until you're confident in your application's environment. Debugging a huge application that explodes in the remote build phase is super annoying and difficult.

### Creating a new AWS App Runner GitHub connector integration

If you need to create a new connector, you need to go to the App Runner services page and go like you're going to create a new service. From that page you can add a new runner connection. You can then leave the page and no sevice will be built, but the new connector will remain. You should only need to do this if you want to allow access to some other non-organization repo.

### Minimum IAM User Policy Permissions

Here is the minimum policy JSON you'll need to attach to a new IAM user:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "apprunner:*",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action":[
                "iam:PassRole",
                "iam:CreateServiceLinkedRole"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::<<AwsAccountNumber>>:role/app-runner-service-role"
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken"
            ],
            "Resource": "*"
        }
    ]
}
```

Make sure to make the replacements to the `Resource` string.


[gh-apps-console]: https://github.com/settings/installations/
    "GitHub application integrations console"

[gh-integrations-console]: https://us-east-1.console.aws.amazon.com/apprunner/home?region=us-east-1#/connections
    "App Runner GitHub integrations console"

[app-runner]: https://aws.amazon.com/apprunner/
    "AWS App Runner"

[app-runner-deploy-template]: https://github.com/thecityny/app-runner-deploy-template
    "App Runner GitHub Action Template"

[pixel-dashboard]: https://github.com/thecityny/pixel-dashboard
    "Pixel Dashboard GitHub Repo"
