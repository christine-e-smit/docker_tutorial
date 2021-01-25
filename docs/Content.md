# Tutorial Content

## Multi-stage builds

You can describe many different containers in the same Dockerfile by using
multi-stage builds. This example illustrates how you might separate out
a base container with all 3rd party libraries installed and then two
containers built on that base image: a production container with just the
code needed to run something operationally and a development container with
additional development tools like editors, linters, and so on.

## Mounting an external directory inside the container

There are all kinds of reasons why mounting external directories or files
inside containers is useful. This example shows how you can (1) mount a
directory with large files into the container so you don't have to make
unnecessary copies and (2) use that mounted directory to get easy access to
files created by scripts run in the container.

## Regridding with Climate Data Operators (CDO)

CDO (https://code.mpimet.mpg.de/projects/cdo/) is a set of command line tools.
It is used to regrid MERRA files in `regrid.py`. Code in this script was
shamelessly copied from Thomas Hearty.

## Plotting with Matplotlib and Cartopy

Matplotlib (https://matplotlib.org/) and a general purpose plotting library and
Cartopy (https://scitools.org.uk/cartopy/docs/latest/) a geospatial library.
They are used by `plot.py` to draw data on maps.
