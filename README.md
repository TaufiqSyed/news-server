# Dubai Tribune: News Aggregator Backend

Built with newsapi.org

## Set-up instructions

1. Use WSL or a Linux/UNIX based OS as Redis is unavailable on Windows
2. Install PostgreSQL and Redis on your machine
3. Update settings.json with your corresponding PostgreSQL username, password, host, and your Redis host as well. The repo is set up with postgres as the username and password.
4. Using `pqsl` run `create database news_database`
5. Clone the GitHub repository from here https://github.com/TaufiqSyed/news-server
6. Open the project directory: `cd news-server`
7. Create a python virtual environment using `python -m venv .venv`
8. Activate the virtual environment using `source .venv/bin/activate`
9. Open https://newsapi.org/ and get an API key after creating an account. Set your environment variable “NEWS_API_KEY” to that value
10. Run `pip install -r requirements.txt`
11. Run `python3 manage.py migrate`
12. Run `python3 manage.py news_api makemigrations`
13. Run `python3 manage.py news_api migrate`
14. Run `python3 manage.py runserver`
15. Open localhost:8000/api/v1/[query_parameters] for API
