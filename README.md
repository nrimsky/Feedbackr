# Feedbackr

## What is this?

An app that enables users to easily collect yes/no feedback on language model outputs from humans for simple finetuning applications.

Currently not deployed anywhere but can easily be at some point :D

## Development

### Database migrations

```bash
python manage.py makemigrations getfeedback # If no migrations yet, or need new ones
python manage.py migrate
```

### Run development server

```bash
python manage.py runserver
```

### Make admin user

```bash
python manage.py createsuperuser
```
