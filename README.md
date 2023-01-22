# Feedbackr

## What is this?

An app that enables users to easily collect yes/no feedback on language model outputs from humans for simple finetuning applications.

## Development

### Database migrations

```bash
cd feedbackr
python manage.py makemigrations getfeedback # If no migrations yet, or need new ones
python manage.py migrate
```

### Run development server

```bash
cd feedbackr
python manage.py runserver
```

### Make admin user

```bash
cd feedbackr
python manage.py createsuperuser
```