# Docker tutorial example

This project has an example Dockerfile that can be used to build a container
that regrids and plots a MERRA-2 M2IMNPASM (doi:10.5067/2E096JV59PK7) granule
to an AIRS L3 grid using cdo.

Many thanks to Thomas Hearty for suggesting this use case and Mahabaleshwara
Hegde for suggesting plotting.

## Content

### Multi-stage builds

You can describe many different containers in the same Dockerfile by using
multi-stage builds. This example illustrates how you might separate out
a base container with all 3rd party libraries installed and then two
containers built on that base image: a production container with just the
code needed to run something operationally and a development container with
additional development tools like editors, linters, and so on.

### Mounting an external directory inside the container

There are all kinds of reasons why mounting external directories or files
inside containers is useful. This example shows how you can (1) mount a
directory with large files into the container so you don't have to make
unnecessary copies and (2) use that mounted directory to get easy access to
files created by scripts run in the container.

### Regridding with Climate Data Operators (CDO)

CDO (https://code.mpimet.mpg.de/projects/cdo/) is a set of command line tools.
It is used to regrid MERRA files in `regrid.py`. Code in this script was
shamelessly copied from Thomas Hearty.

### Plotting with Matplotlib and Cartopy

Matplotlib (https://matplotlib.org/) and a general purpose plotting library and
Cartopy (https://scitools.org.uk/cartopy/docs/latest/) a geospatial library.
They are used by `plot.py` to draw data on maps.

## Running this tutorial

### Step 1: Get MERRA data

You will need to download at least one MERRA granule and put it under work_area/downloads.
NetCDF files can be found here:
https://goldsmr5.gesdisc.eosdis.nasa.gov/data/MERRA2_MONTHLY/M2IMNPASM.5.12.4/.
I got the January 1980 granule,
https://goldsmr5.gesdisc.eosdis.nasa.gov/data/MERRA2_MONTHLY/M2IMNPASM.5.12.4/1980/MERRA2_100.instM_3d_asm_Np.198001.nc4

### Step 2: Build the "production" container

In production, you want to have all your scripts and libraries installed in
standard locations. The `prod` stage of the `Dockerfile` builds on top
of the `base` layer to install `regrid.py` and `plot.py`.

This Dockerfile is an _example_, not a real production-ready image. A real
production image would need to have some kind of http server to accept job
requests or some kind of script to fetch job requests from elsewhere.

To build the prod stage of the container, run:

```bash
docker build --target prod -t docker_tutorial_prod .
```

from the top level directory of this repository.

Breaking down the command:

1. `docker` - calls the docker daemon.
2. `build` - tells docker to build an image.
3. `--target prod` - tells docker to build the target called `prod`.
4. `-t docker_tutorial_prod` - tells docker to call the image
`docker_tutorial_prod`.

### Step 3: Regrid a file using the "production" container

If you used something other than the January 1980 granule, adjust the filenames
accordingly. From the top level of the repository, call:

```bash
docker run --rm --volume "$PWD"/work_area/:/work_area docker_tutorial_prod regrid.py /work_area/downloaded/MERRA2_100.instM_3d_asm_Np.198001.nc4 /work_area/regridded/out.nc4
```

If you look under `work_area/regridded`, you should now see `out.nc4`.

Breaking down the command:

1. `docker` - calls the docker daemon.
2. `run` - tells docker to run (instantiate) a docker image
3. `--rm` - tells docker to get rid of the instantiated image when it exits
4. `--volume` - tells docker to mount directory `"$PWD"/work_area/` as
`/work_area` inside the container.
5. `docker_tutorial_prod` - tells docker which image to instantiate.
6. `regrid.py /work_area/downloaded/MERRA2_100.instM_3d_asm_Np.198001.nc4 /work_area/regridded/out_198001.nc4` -
tells docker what command to run inside the container. Note that the paths
passed to regrid.py reference the internally mounted directory, `/work_area`.

### Step 4: Plot the regridded file using the "production" container

From the top level of the repository, call:

```bash
docker run --rm --volume "$PWD"/work_area/:/work_area docker_tutorial_prod plot.py /work_area/regridded/out.nc4 /work_area/plots/out.png T 0
```

You should see an `out.png` file in the `work_area/plots directory`.

Breaking down this command:

1. `docker` - calls the docker daemon.
2. `run` - tells docker to run (instantiate) a docker image
3. `--rm` - tells docker to get rid of the instantiated image when it exits
4. `--volume` - tells docker to mount directory `"$PWD"/work_area/` as
`/work_area` inside the container.
5. `docker_tutorial_prod` - tells docker which image to instantiate.
6. `plot.py /work_area/regridded/out.nc4 /work_area/plots/out.png T 0` -
tells docker what command to run inside the container. Again, note that the
paths reference the internally mounted directory.
