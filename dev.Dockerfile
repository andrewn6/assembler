FROM python:3.8

# Meta data:
LABEL maintainer="matthewgleich@gmail.com"
LABEL description="PROJECT_DESCRIPTION"

# Copying over all the files:
COPY . /usr/src/app
WORKDIR /usr/src/app

# Installing dependencies:
RUN python -m pip install --upgrade pip
RUN pip3 install poetry==1.0.10
RUN poetry config virtualenvs.create false
RUN poetry install --no-root -n

CMD ["make", "local-test"]
