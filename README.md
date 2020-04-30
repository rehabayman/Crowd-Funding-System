# Crowd Funding System #

It is a Web Application for automating the projects' funding activity. It has two views the admin and user views.

## Getting Started ##
These steps will get you a copy of the project up and running for development and testing purposes.

## Installation ##

1. Install **Python >= 3.x**
2. Install **pip3**
3. Install **mySql** or **mariaDB**
4. Clone the Project
5. Create Python Virtual Environment
	```bash
		python3 -m venv develop-env ## For Creating
		source develop-env/bin/activate ## For Activating
		## For Deactivating the Virtual Environment
		deacivate
	```
6. Run the Following Command to install the dependencies [*make sure the virtual environment is activated*]
	```bash
		pip3 install -r requirements.txt
	```
7. Create an empty database with named **crowd_funding_system** in your database engine.
8. In the settings.py file change the `HOST`, `USER`, and `PASSWORD` options to match the credentials of the database you just created. This will allow us to run migrations in the next step.
9. Run the following:
	```bash
		python3 manage.py migrate
	```

## Usage ##

Run the following command to launch the app:
	``
	python3 manage.py runserver
	``

## Admin Features 

1. Choose Projects to be Featured.
2. View and Delete Reported Comments / Projects.
3. CRUD Operations on Projects Categories.

## User Features

1. Update his Profile Data.
2. Create Projects.
3. View Projects.
	- Search by: title / tag.
	- Filter by Category 
4. Rate Projects.
5. Add Comments on Projects.
6. Add Comments' Replies on Projects.
7. Donate to Projects.
8. View his Projects and Donations.

## Built With

[Django](https://www.djangoproject.com/)


## Authors

1. [Mohamed Adham](https://github.com/mohamedadham)
2. [Mohamed Tarek](https://github.com/M-tarek93)
3. [Rehab Ayman](https://github.com/rehabayman)
4. [Mohamed Zakaria](https://github.com/Mohamed-Zkaria)
5. [Nouran M.Yehia](https://github.com/Nouran-yehia)
