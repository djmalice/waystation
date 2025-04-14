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

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
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

## License
This project is licensed under the MIT License. See the LICENSE file for details.