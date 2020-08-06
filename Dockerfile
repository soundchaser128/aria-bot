FROM python:3.8

WORKDIR /app

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

COPY . .
CMD ["python", "bot.py"]