FROM python:3.8

ARG REQUIREMENTS_FILE

WORKDIR /custom-extraction

COPY ./requirements/ ./requirements
RUN pip install -r ./requirements/${REQUIREMENTS_FILE}
RUN python -c "import nltk;nltk.download('punkt')"

COPY . .

EXPOSE 5006

CMD [ "python", "./run.py" ]