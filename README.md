# Waystation RFQ Portal

The Waystation RFQ Portal is a Django-based web application designed to streamline the process of managing RFQs (Request for Quotations) and supplier interactions. It provides features for creating, processing, and managing RFQs, as well as supplier details and quotes.

## Features
- Create and manage RFQs
- Process supplier emails to extract structured data
- View and manage supplier details
- Submit and review quotes

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

## License
This project is licensed under the MIT License.