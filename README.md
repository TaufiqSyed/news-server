Set-up instructions

Use WSL or a Linux/UNIX based OS as Redis is unavailable on Windows
Install PostgreSQL and Redis on your machine
Update settings.json with your corresponding PostgreSQL username, password, host, and your Redis host as well. The repo is set up with postgres as the username and password.
Using `pqsl` run `create database news_database`
Clone the GitHub repository from here https://github.com/TaufiqSyed/news-server
Open the project directory: `cd news-server`
Create a python virtual environment using `python -m venv .venv`
Activate the virtual environment using `source .venv/bin/activate`
Open https://newsapi.org/ and get an API key after creating an account. Set your environment variable “NEWS_API_KEY” to that value
Run `pip install -r requirements.txt`
Run `python3 manage.py migrate`
Run `python3 manage.py news_api makemigrations`
Run `python3 manage.py news_api migrate`
Run `python3 manage.py runserver`
Open localhost:8000/api/v1/[query_parameters] for API
