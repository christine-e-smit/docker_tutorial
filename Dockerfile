###############################################################################
# Base image with just the stuff we might need to run this in a container
# against lots and lots of data.
###############################################################################
FROM continuumio/miniconda3 as base

RUN conda install -y -c conda-forge cdo

###############################################################################
# Development container with some of the tools we might want to run during
# development
###############################################################################
FROM base as dev

RUN conda install -y pytest pylint black ipython