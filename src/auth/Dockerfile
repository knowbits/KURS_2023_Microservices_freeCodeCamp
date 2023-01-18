# ===========================================
# NOTE: Each instruction in a "Dockerfile" will create a new "image layer"
#       => Upon rebuild, Docker will use cahced image layers.
#
# Build the image with one of these commands:
#   $ docker build .
#   $ docker build . --tag eb_auth_python:v0.1
#
# PREPARATION STEPS:
#   Make sure to activate the "Python virtual environment" previously created:
#     $ source ./venv/bin/activate
#   Verify it : $ env | grep VIRTUAL
#
# FUTURE: A more modern approach for DEPENDENCIES seems to be
#         to use "Pipenv" (and "Pipfile") instead of "requirements.txt".
#
#    => Using "Pipenv" with Docker is described here:
#       https://pipenv.pypa.io/en/latest/basics/#pipenv-and-docker-containers
# ===========================================

# Find the version of Python: `$ python3 --version`  # => Python 3.10.7
FROM python:3.10-slim-bullseye

# We use "&&"" to assemble several build steps into the same "image layer":
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

# The location of the applications source code:
WORKDIR /app

# DOES NOT WORK PROPERLY: To create the "python dependencies" file, run:
#   $ pip freeze > requirements.txt
#   => PROBLEM: Includes all Python packages installed on the system!!
#
# => Better approach: Use "pipreqs" to generate "requirements.txt"
#    https://github.com/bndr/pipreqs
#    "Generate pip requirements.txt file based on imports of any project."
#    Run: $ pipreqs .
#
# FUTURE: Use "virtualnv" with these approaches:
#    1) Use "Pipenv" or 2) "Conda"
#    NOTE: "requirements.txt" is obsolete => Use "Pipenv" (creates "Pipfile")
COPY ./requirements.txt /app

# "pip install" is one of the most time consuming build steps:
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Docker will detect if there is a change in our source code, and rebuild from here:
COPY . /app

# The port that will be published from the Docker container:
EXPOSE 5000

# Same as running: $ python3 server.py :
CMD ["python3", "server.py"]
