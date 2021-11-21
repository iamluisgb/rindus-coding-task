# Rindus Bank

This app is available in: www.raiatech.com

## Requirements

Implement a small Django application to manage (CRUD) users and their bank account data (IBAN). Required fields are first name, last name and IBAN. Data should be validated.

- Administrators of the app should authenticate using a Google account
- Administrators should be able to create, read, update and delete users
- Restrict manipulation operations on a user to the administrator who created them
- Use PostgreSQL as the database backend
- Use Python 3.x
- Write documentation on how to setup, run and use your implementation

Test environment

- Set up a virtual machine environment using docker-compose to run the test task including some short documentation

## Development

To start working on this project just run:

```bash
docker-compose -f local.yml build
docker-compose -f local.yml up
```

# Testing

To run test execute:

```bash
docker-compose -f local.yml run --rm django pytest
```

# Deploy in AWS

Although here we will be using AWS, migrating our stack to any other cloud platform with any other OS does not involve any substantial effort.

## Setup

### AWS(EC2)

In this read we will work with Ubuntu Server. The steps you must follow are:

- Launch instance.
  During instance launch you must:
- Assign a role that has the permission AmazonS3FullAccess
- Make sure that the security group of the instance has ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) open.
- Configure EC2 instance
  Connect to your EC2 instance and update the server packages with the commands:
  `bash sudo apt-get update -y sudo apt-get upgrade -y `

### Docker

You need to install Docker and Docker Compose.
You can follow this documentation: https://docs.docker.com/engine/install/ubuntu/

### Git

Run:

```bash
sudo apt-get install
```

Copy the repository:

```bash
sudo git clone ...
```

### Domain

The specific configuration of the DNS records for the domain varies by provider but actually translates into creating the following 2 records:

- A | www | IP
- A | @ | IP

Which means that you will create two records of type ADDRESS for your naked domain ( domain.com ) and your www subdomain ( www.domain.com ) and both will point to the IP of the instance.
When you are making the configuration keep in mind that this change can take between 5 minutes and 48 hours.

## Installing the app

Before you start, check the file production.yml in the root of the project. This file has all necessary configuration to start the application and includes the following services:

- django: The application running low Gunicorn.
- postgres: PostgreSQL database with application data.
- redis: A Redis instance for cache.
- caddy: An HTTP server that will be in charge of receiving requests from outside and uses HTTPS by default.
- celeryworker: Celery's worker runs.
- celerybeat: Run Celery's beat.
- flower: Run Flower , a tool to visualize celery on the web

### Environment variables

First we need a folder to store them, which we can get by running (inside /home/ubuntu/rindus)

```bash
mkdir -p .envs/.production
```

For our application to work we need the following variable files:

```bash
touch .envs/.production/.django
touch .envs/.production/.postgres
touch .envs/.production/.caddy
```

And inside each one, with your favorite text editor (vi or nano), write the following variables

```
# .postgres

# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=cride
POSTGRES_USER=SECURE_USER
POSTGRES_PASSWORD=SECURE_PASSWORD
```

```
# .django

# Django
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=SECURE_SECRET_KEY

# Static files
DJANGO_AWS_STORAGE_BUCKET_NAME=S3_BUCKET_NAME

# Admin
DJANGO_ADMIN_URL=SECURE_ADMIN_URL

# E-Mail
MAILGUN_API_KEY=SECRET_KEY
MAILGUN_DOMAIN=SECRET_KEY


# Redis
REDIS_URL=redis://redis:6379/0

# Flower
CELERY_FLOWER_USER=SECURE_USER
CELERY_FLOWER_PASSWORD=SECURE_PASSWORD
```

```
DOMAIN_NAME=raiatech.com
```

It is VERY IMPORTANT that you notice that some of the variables do not have values
and it is your job to put real and safe values.

## Launch

Build the stack with `sudo docker-compose -f production.yml build`.
Now we can initialize the database with `docker-compose -f production.yml run --rm django python manage.py migrate`
We can create a super user with `sudo docker-compose -f production.yml run --rm django python manage.py createsuperuser`
We run the application with `sudo docker-compose -f production.yml up`

## User Registration using Goole OAuth

Open Authorization (OAuth) is a service that allows websites or apps to share user information with other websites without being given a users password. To integrate Google OAuth features in this app, we use [django-auth](https://django-allauth.readthedocs.io/en/latest/installation.html).

It is necessary to create a Google App to obtain a key/secret pair. Go to the Google Developers Console and click on Create Project. Choose a name for your project and an ID.

Next, click on your newly created project and on the left menu select APIs & auth –> Credentials and click on the Consent screen tab. You should provide at least a Name and an Email.
Go back to the Credentials tab and click on Create new Client ID. Select Web Application and use:

Authorized Javascript Origins: (YOUR DOMAIN)

Authorized Redirect Uris: (YOUR DOMAIN)/accounts/google/login/callback/

Now Create a Social Application for Google at (YOUR DOMAIN)/admin/socialaccount/socialapp, with the following properties:

- Provider: Google
- Name: Google (or something similar)
- Client ID: your application Client ID (obtained in the Developers Console at APIs & auth –> Credentials).
- Secret Key: your application Client Secret
- Key: not needed (leave blank).
- Select the corresponding site.

## Installing and configuring supervisor

Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems. Supervisor allos us to register our application as a Systemd service. To do this we have to follow the following steps:

- install supervisor: `sudo apt-get install supervisor -y`
- Login as super user: `sudo su`
- Create the file rindus.conf inside /etc/supervisor/conf.d/ with the following content:
  ```
  [program:rindus]
  command=docker-compose -f production.yml up
  directory=/home/ubuntu/rindus
  redirect_stderr=true
  autostart=true
  autorestart=true
  priority=10
  ```
- Register the service in supervisor with `supervisorctl reread` and `supervisorctl update`
- Start the service with `supervisorctl restart rindus`
- Verify that the service is running with `supervisorctl status`

We can verify that everything is working correctly restarting the server from AWS.
