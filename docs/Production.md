# Build and run the "production" container

In production, you want to have all your scripts and libraries installed in
standard locations. The `prod` stage of the `Dockerfile` builds on top
of the `base` layer to install `regrid.py` and `plot.py`.

This Dockerfile is an _example_, not a real production-ready image. A real
production image would need to have some kind of http server to accept job
requests or some kind of script to fetch job requests from elsewhere.

## Build

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
5. `.` - tells docker to build the current directory.

## Regrid

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

## Plot

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
