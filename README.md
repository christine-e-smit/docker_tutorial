# Docker tutorial example

This project has an example Dockerfile that can be used to build a container
that regrids and plots a MERRA-2 M2IMNPASM (doi:10.5067/2E096JV59PK7) granule
to an AIRS L3 grid using cdo.

Many thanks to Thomas Hearty for suggesting this use case and Mahabaleshwara
Hegde for suggesting plotting.

1. [Introduction](docs/Content.md)
2. [Get MERRA data](docs/GetData.md) <-- Do this before you try to run the tutorial!
3. [Build and run the "production" container](docs/Production.md)
4. [Develop inside a container](docs/Develop.md)
