# aiml-lab-e-waste


### Virtual Environment

1. `pip install virtualenv`
2. `virtualenv ENV_name`
3. `source ENV/bin/activate` 
4. `docker build`

After intitializing the virtual environment move to the folder `python-docker`

### Docker Container

-  Build and image- [for intitialization and downloading dependencies from requirements.txt]
    `docker build --tag python-docker .`

- View Local images-
    `docker images`

- Run docker image- [to run app.py and start the flask app]
    `docker run python-docker`