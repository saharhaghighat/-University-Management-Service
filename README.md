# University Management Service
A University Management Service was developed using Django and Django Rest Framework (DRF) to streamline course enrollment, teacher assignment, and student registration. This project enhanced the team's Python skills and provided practical experience in web development and database management with Django and DRF. 

## Prerequisites

- Python (version specified in `pyproject.toml`)
- Poetry (for dependency management)

## Setup

### Using Poetry

1. **Install Dependencies**: First, you need to install the project dependencies. Navigate to the project's root directory and run:
   ```sh
   poetry install --with dev
   ```

2. **Activate the Virtual Environment**: To activate the Poetry-managed virtual environment, run:
   ```sh
   poetry shell
   ```

3. **Database Migrations**: Apply the database migrations with:
   ```sh
   python manage.py migrate
   ```

4. **Run the Development Server**: Start the development server using:
   ```sh
   python manage.py runserver
   ```

NOTE: You can use the commands without activating `poetry shell` like so:
```sh
poetry run python manage.py runserver
```

### Using Standard Python Environment

1. **Virtual Environment**: Create a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

2. **Install Dependencies**: Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. **Database Migrations**: Apply the database migrations:
   ```sh
   python manage.py migrate
   ```

5. **Run the Server**: Start the development server:
   ```sh
   python manage.py runserver
   ```

