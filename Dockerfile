###############################################################################
# Base image with cdo and required packages
###############################################################################
FROM continuumio/miniconda3 as base

RUN conda install -y -c conda-forge cdo

WORKDIR /
COPY requirements.txt .
RUN conda install -y -c conda-forge --file requirements.txt
RUN rm requirements.txt

###############################################################################
# Production image with the scripts installed in a standard directory.
###############################################################################
FROM base as prod

RUN mkdir /tmp/install
WORKDIR /tmp/install
COPY setup.py .
COPY regrid.py .
COPY README.md .
COPY requirements.txt .
RUN python setup.py install

WORKDIR /
RUN rm -rf /tmp/install

###############################################################################
# Development container with some of the tools we might want to run during
# development. The assumption is that you will mount the code into the dev
# container, so there's no need to copy the code into the container.
###############################################################################
FROM base as dev

# Install git-secrets, which can be used as a git hook to prevent you from
# accidentally checking in files with AWS secrets like keys. (This tutorial
# does not include anything related to AWS, but this is useful if you have
# automatically configured all git repositories to use git-secrets.)
RUN apt-get update
RUN apt-get install make
RUN mkdir /tmp/secrets
WORKDIR /tmp/secrets
RUN git clone https://github.com/awslabs/git-secrets.git
WORKDIR /tmp/secrets/git-secrets
RUN make install
RUN apt-get -y remove make
WORKDIR /
RUN rm -rf /tmp/secrets

# Install editors, if that's what you like to use. I use Visual Studio Code,
# which is why you'll see devcontainer.json and settings.json in this
# repository.
RUN apt-get install vim
RUN apt-get install emacs

# pytest: unit testing
# pylint: static code linting
# black: code formatting
# ipython: a better command line for python
RUN conda install -y pytest pylint black ipython
# pipreqs: useful for deriving required packages
RUN conda install -y -c conda-forge pipreqs