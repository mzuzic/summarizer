FROM art01-ic-devops.jfrog.io/ic-python-jedi-builder:3.8.1
WORKDIR /pythonapp
COPY . .
EXPOSE 5002
CMD [ "python", "./pythonapp/run.py" ]