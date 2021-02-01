# Develop inside a container

Developing inside a container is great. As you write and run your code, you
get the context of the container environment. So linters can make sure you
aren't trying to use libraries that aren't installed. Code sense can help
you with function hints and completion. Unit tests can be run and debugged.

## Build the development container

To build the dev (last) stage of the Dockerfile, run:

```bash
docker build -t docker_tutorial_dev .
```

from the top level of the repository. Note that we don't have to specify the
stage name because `dev` is the last stage in the file.

Breaking down the command:

1. `docker` - calls the docker daemon.
2. `build` - tells docker to build an image.
3. `-t docker_tutorial_dev` - tells docker to call the image
`docker_tutorial_dev`.
4. `.` - tells docker to build the current directory.

## Old School: vi/emacs

I've installed vi and emacs in the development container for those who want to
give these a try.

To get a command line inside the container with the current directory
mounted in the container under /workspaces/docker_tutorial, run:

```bash
docker run --rm -it --volume "$PWD":/workspaces/docker_tutorial docker_tutorial_dev bash
```

You should get a command prompt inside the container. Go wild! You can do
anything you would normally do at a bash prompt. Use vi/emacs to edit
something. Run the scripts. Knock yourself out. Use `exit` to get out of the
container.

Breaking down the command:

1. `docker` - calls the docker daemon
2. `run` - tells docker to run (instantiate) a docker image
3. `--rm` - tells docker to get rid of the instantiated image when it exits
4. `-it` - these two options together allow you to get a command prompt inside
the container.
5. `--volume` - tells docker to mount directory `"$PWD"` as
`/workspaces/docker_tutorial` inside the container.
6. `docker_tutorial_dev` - tells docker which image to instantiate.
7. `bash` - tells docker to run bash, which gives you the command prompt. If
bash doesn't float your boat, install your favorite shell (e.g. -
add `RUN apt-get install -y zsh` in the dev section of the Dockerfile) and
call that instead.

## Visual Studio Code

We are planning to do an entire tutorial on development tools. But this will
give you an introduction to using Visual Studio Code's remote development
capability. I actually used VSC (and a some jupyter notebook) to
create this tutorial. The secret sauce here is the
`.devcontainer/devcontainer.json` file. This tells VSC what container to use.
The `.vscode/settings.json` file contains standard VSC configuration.

To get started, open VSC select the root directory of this repository. On the
lower left, you should see a green rectangle with greater than and less than
symbols. Click on there and select `Remote-Containers : Reopen in Container`.

For more information, read VSC's documentation:
[https://code.visualstudio.com/docs/remote/containers](https://code.visualstudio.com/docs/remote/containers).
