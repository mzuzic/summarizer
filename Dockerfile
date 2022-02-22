FROM python:3.8

ARG REQUIREMENTS_FILE

WORKDIR /custom-extraction

COPY ./requirements/ ./requirements
RUN pip install --upgrade pip
RUN pip install -r ./requirements/${REQUIREMENTS_FILE}

RUN set -x && \
	apt-get update && \
	apt -f install	&& \
    apt -y install wget && \
	apt-get -qy install netcat && \
	rm -rf /var/lib/apt/lists/* && \
	wget -O /wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && \
	chmod +x /wait-for

RUN python -c "import nltk;nltk.download('punkt')"

COPY . .

EXPOSE 5006

CMD [ "python", "./run.py" ]