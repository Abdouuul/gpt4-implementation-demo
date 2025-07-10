### GPT4 Mini implemenation project

-> Backend using Django Python

-> Frontend using React

This is a demo using Gpt4 mini via the Microsoft Azure AI Foundry Platform, API key secured in a .env file create and saved locally.
The purpose of this application is to write emails in different styles, languages, and contexts then configure the output using structured output reponses via pydantic.

To run this application, please run the following commands :

```
python -m venv .venv
pip  install -r requirements.txt
```

Then

```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

and finally

```
cd frontend
npm install
npm run dev
```
