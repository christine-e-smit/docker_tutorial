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
# Create a production container with the regrid script installed in a standard
# directory.
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
# development.
###############################################################################
FROM base as dev

# Install git-secrets, which can be used as a git hook to prevent you from
# accidentally checking in files with AWS secrets like keys. (This tutorial
# does not include anything related to AWS, but this is useful if you have
# automatically configured all git repositories to use git-secrets.)
RUN apt-get install make
RUN mkdir /tmp/secrets
WORKDIR /tmp/secrets
RUN git clone https://github.com/awslabs/git-secrets.git
WORKDIR /tmp/secrets/git-secrets
RUN make install
RUN apt-get -y remove make
WORKDIR /
RUN rm -rf /tmp/secrets

# pytest: unit testing
# pylint: static code linting
# black: code formatting
# ipython: a better command line for python
RUN conda install -y pytest pylint black ipython
RUN conda install -y -c conda-forge pipreqs