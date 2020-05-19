

Developer guide
============

* Set up virtualenv & install python module dependencies
* Install docker / Kubernetes
* UML Class diagrams
* Developer workflow
   * Python-only
   * Docker
   * Kubernetes
   * Versioning & Releases 




### Python prerequisites ### 

It is recommended that you use something like virtualenv / pipenv to ensure you have a clean Python environment and reduce the risk of causing damage to existing tooling & applications

Install python 3.x (varies depending on platform)

Install & configure virtualenv:
```console
python3 -m pip install --upgrade pip
pip3 install virtualenv
# Find the your python version & path
which python3
mkdir -p $HOME/virtualenvs/python3 && cd "$_"
virtualenv -p python3 py3-imagechecker
source py3-imagechecker/bin/activate
# ^ it is advised to put the above (using the full path) in your bashrc/zshrc so it loads on each shell spawning
```

### Docker installation ###

Follow the instructions:
* For OS X: https://docs.docker.com/docker-for-mac/install/
* For Windows: https://docs.docker.com/docker-for-windows/install/

(Enable Kubernetes for either platform)

https://docs.docker.com/docker-for-windows/#kubernetes

https://www.docker.com/blog/docker-windows-desktop-now-kubernetes/

### Docker compose installation ###

The makefile includes tasks related to building & deploying a docker image with the ImageChecker module. Doing so requires docker-compose installed. This can be achieved in multiple ways.

https://github.com/Yelp/docker-compose/blob/master/docs/install.md

To verify docker-compose is working, execute the compose-dump task from within the imagechecker directory, where the Makefile resides:

```console
$ make compose-dump
docker-compose config
services:
  imagechecker:
    build:
      context: /tmp/imagechecker
    image: nkaravias/imagechecker:snapshot
    volumes:
    - /tmp/tests/docker:/opt/imagechecker/etc:rw
    - /tmp/tests/assets/images:/images:rw
    - /tmp/out:/opt/imagechecker/out:rw
version: '3.0'
```

### UML Class Diagrams ###

UML class diagrams have been generated using pyreverse and are stored in the [docs/developer/uml](uml) directory

### Build & Run (Python) ###

Make run will simply run the python interpreter against imagechecker/main.py, which is the entrypoint of the module.

By default ImageChecker will use a configuration from [conf/config.yaml](../../conf/config.yaml) to specify the [input.csv](../../examples/input.csv) (containing the image pairs) and the output location for the processing results.

To add new image pairs or combinations of existing ones, modify [examples/input.csv](../../examples/input.csv). 

Output results are by default stored in [out/output-test.csv](../../out/output-test.csv).

Example execution:
```console
➜  imagechecker git:(dev-something) ✗ make run
python imagechecker/main.py
2020-05-19 13:39:08,079:INFO:config: [config.py:19] ImageChecker config set to: /workspace/python/imagechecker/conf/config.yaml
2020-05-19 13:39:08,080:INFO:__main__: [main.py:23] Input csv path:examples/input.csv
2020-05-19 13:39:08,080:INFO:__main__: [main.py:25] Output csv path:output-test.csv
2020-05-19 13:39:08,080:INFO:__main__: [main.py:26] Image whitelist:['gif', 'pbm', 'pgm', 'ppm', 'tiff', 'webp', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'exr']
2020-05-19 13:39:08,129:INFO:config: [config.py:96] Valid input configuration:examples/input.csv
2020-05-19 13:39:08,129:INFO:config: [config.py:102] Writing to ouput: image1 image2 similarity elapsed
2020-05-19 13:39:08,163:INFO:config: [config.py:102] Writing to ouput: image1.jpg image2.jpg 0.254 27
2020-05-19 13:39:08,181:INFO:config: [config.py:102] Writing to ouput: image1.png image3.jpg 0.296 11
2020-05-19 13:39:08,194:INFO:config: [config.py:102] Writing to ouput: image1.jpg image1_png.png 0 8
2020-05-19 13:39:11,452:INFO:config: [config.py:102] Writing to ouput: image7.jpg image7_large.png 0.616 3251
2020-05-19 13:39:15,512:INFO:config: [config.py:102] Writing to ouput: image8.jpg image8.png 0.986 4048
```

### Build & Run (Docker) ###

Instead of running the module by invoking python locally, there are two tasks that will help in building a docker image and executing it

```console
make docker-build
```
The docker-build task will execute docker-compose with the build directive. This will create a docker image using the [Dockerfile](../../Dockerfile) and version it as per the tag located in [.env](../../.env). Modifying the contents of the .env file will update the version of the next docker image that gets built.

```console
make docker-run
```

The docker-run task will run docker-compose with the purpose of executing the ImageChecker image built previously. As a best practice, __no configuration or data is baked inside the docker image itself__. As a result, to properly execute ImageChecker we need to pass during runtime three pieces of information:
* The config.yaml that specifies where input.csv is located, the actual image pairs in scope and where the output-test.csv will be located

We also need to ensure that output-test.csv can be accessed from outside the docker container for the developer.

To achieve the above, we are running docker-compose by providing three volumes as you can see by the compose configuration. All volumes are configurable and live wherever imagechecker.git is checked out

```console
version: '3'

services:
  imagechecker:
    image: nkaravias/imagechecker:${TAG}
    build: .
    volumes:
     - ./tests/docker:/opt/imagechecker/etc
     - ./tests/assets/images:/images
     - ./out:/opt/imagechecker/out
```

**IMPORTANT**
Due to difficulties in getting Docker volumes to get properly mounted using Windows/WSL, execute the ```make docker-run``` task from an instance of Powershell (if on Windows). The ```make docker-build``` still works from WSL (if on Windows)


### Build & Run (Kubernetes) ###

In order to develop ImageChecker in a more controlled way, a Kubernetes workflow is also included. This allows for the ```make docker-build``` to be executed locally (to build the docker image)

The [tests/kubernetes](../../tests/kubernetes) directory contains the required Kubernetes manifests for creating a development namespace where a Kubernetes Job (using the nkaravias/imachecker:<tag> image) can be executed:
* namespace.yaml (The imagechecker-dev namespace)
* quota.yaml (A resource quota for the namespace workloads)
* sa.yaml (The service account under which ImageChecker Job will run as)
* job.yaml (The ImageChecker job)

Sample images have been converted into Kubernetes ConfigMaps and a sample configuration (similar to [tests/docker/config.yaml](../../tests/docker/config.yaml)) is also presented
* cfg-config.yaml
* cfg-input.csv.yaml (Modify to add more image configmaps)
* cfg-image2.jpg.yaml
* cfg-image1.ping.yaml

** DISCLAIMER ** It is a bad practice to try to store large binary files as Kubernetes configmaps. Large images are a bad use case for ConfigMaps. The point of doing this is to show the flexibility of using Kubernetes as a development environment vs manually orchestrating docker executions. Ideally the images would be presented to Kubernetes in a volume and access directly from whatever workload requires them (Job/Deployment etc).

The ```k8s-run``` make task will do the following
```console
k8s-run:
	@make -s docker-build
	kubectl apply -f tests/kubernetes/
	kubectl wait --for=condition=complete job/imagechecker --timeout=60s -n imagechecker-dev
	kubectl logs job/imagechecker -n imagechecker-dev
```

* It will invoke the docker-build task that will build a new image
* It will kubectl apply the test manifests and will create a new namespace and deploy the imagechecker job
* Once the imagechecker job is completed it will execute ```kubectl logs``` to get the output of the job

### Versioning & Releases ###

Ideally a github action would be configured to ensure that a docker build & unit tests are executed after each commit. However no CI process has been created. As a result, versioning, tagging & releasing versions to users are a manual process.

The version of each docker image is controlled by the [.env](../../.env) TAG property. Ideally a CI system would be responsible for verstioning and tagging an image that is ready to be released. For snapshot builds its recommended that the commit SHA is used.

