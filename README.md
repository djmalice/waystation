# Waystation RFQ Portal

The Waystation RFQ Portal is a Django-based web application designed to streamline the process of managing RFQs (Request for Quotations) and supplier interactions. It provides features for creating, processing, and managing RFQs, as well as supplier details and quotes.

## Features
- Create and manage RFQs
- Process supplier emails to extract structured data
- View and manage supplier details
- Submit and review quotes
- Generate email for missing quote details

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- Virtualenv (optional but recommended)
- SQLite (default database)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd waystation
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Rename dummy .env.example file to .env and add openai api key:
   ```bash
   mv .env.example .env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application in your browser at `http://127.0.0.1:8000/`.

## Project Structure
- `compareapp/`: Contains the main application logic, including models, views, templates, and tests.
- `rfqportal/`: Contains project-level settings and configurations.
- `templates/`: Contains HTML templates for the application.
- `static/`: Contains static files like CSS and JavaScript.

## Running Tests
To run the test suite, use the following command:
```bash
python manage.py test
```

## Database Information
The project uses SQLite as the default database. SQLite is a lightweight, file-based database that requires no additional setup. The database file is located at `db.sqlite3` in the project directory.

To set up and apply database migrations, use the following commands:

1. Make migrations (if you have made changes to the models):
   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations to the database:
   ```bash
   python manage.py migrate
   ```

## Setting Up Redis and Celery for Background Tasks

To enable background processing for LLM calls, you need to set up Redis as the message broker and Celery as the task queue.

### Install Redis
1. Install Redis on your system:
   - **macOS**:
     ```bash
     brew install redis
     ```
   - **Ubuntu**:
     ```bash
     sudo apt update
     sudo apt install redis
     ```
   - **Windows**:
     Download and install Redis from the official website: https://redis.io/download

2. Start the Redis server:
   ```bash
   redis-server
   ```

3. Verify that Redis is running:
   ```bash
   redis-cli ping
   ```
   You should see the response: `PONG`

### Install Celery
1. Install Celery and the required dependencies:
   ```bash
   pip install celery[redis]
   ```

2. Configure Celery in your Django project:
   - Open `rfqportal/celery.py` and ensure the following configuration:
     ```python
     from __future__ import absolute_import, unicode_literals
     import os
     from celery import Celery

     # Set the default Django settings module for the 'celery' program.
     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rfqportal.settings')

     app = Celery('rfqportal')

     # Using a string here means the worker doesn't have to serialize
     # the configuration object to child processes.
     app.config_from_object('django.conf:settings', namespace='CELERY')

     # Autodiscover tasks in installed apps
     app.autodiscover_tasks()

     @app.task(bind=True)
     def debug_task(self):
         print(f'Request: {self.request!r}')
     ```

   - In `rfqportal/settings.py`, add the following Celery configuration:
     ```python
     CELERY_BROKER_URL = 'redis://localhost:6379/0'
     CELERY_ACCEPT_CONTENT = ['json']
     CELERY_TASK_SERIALIZER = 'json'
     ```

### Start Celery Workers
1. Open a new terminal and start the Celery worker:
   ```bash
   celery -A rfqportal worker --loglevel=info
   ```

2. (Optional) Start the Celery beat scheduler if you are using periodic tasks:
   ```bash
   celery -A rfqportal beat --loglevel=info
   ```

### Verify the Setup
1. Ensure Redis is running by checking its status or using `redis-cli ping`.
2. Ensure Celery workers are running and connected to Redis.
3. Test a background task by calling a Celery task in your Django shell:
   ```bash
   python manage.py shell
   >>> from compareapp.services import process_email_text
   >>> process_email_text.delay("Test email content", 1)
   ```
   Check the Celery worker logs to confirm the task execution.

## License
This project is licensed under the MIT License.