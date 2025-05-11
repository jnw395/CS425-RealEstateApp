# CS425-RealEstateApp

This is a project with the purpose of creating a real estate management system, specificallyt focusing on rental properties. It manages users, properties, listings, bookings, profiles, and other related data.

## Technologies Used

* Backend: Python (Flask)
* Database: PostgreSQL
* Frontend: HTML, CSS, JavaScript

## Installation

Install the following libraries before running:
```sh
pip install flask
```
```sh
pip install psycopg2
```
```sh
pip install flask
```
```sh
pip install datetime
```
```sh
pip install dotenv
```

* Create a file named `.env` in the project's root directory.
* Add the following variables to the `.env` file, replacing the values with your actual database credentials and other sensitive information:
```
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_NAME=<your_database_name>
DB_HOST=<your_database_host> # e.g., localhost
DB_PORT=<your_database_port> # e.g., 5432
SECRET_KEY=<your_flask_secret_key> #generate a random string using the generate_key.py file (for the purpose of using Flask)
```
        
The site can be ran from running run.py
You can test using these provided credentials:
* Email: john.doe@example.com
* Password: password123
