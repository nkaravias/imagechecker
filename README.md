

BJORN's IMAGE CHECKER
============



Calculate the SSIM difference between a list of image pairs and record the processing time elapsed
----------
 SSIM is used for measuring the similarity between two images. The SSIM index is a full reference metric; in other words, the measurement or prediction of image quality is based on an initial uncompressed or distortion-free image as reference. SSIM is designed to improve on traditional methods such as peak signal-to-noise ratio (PSNR) and mean squared error (MSE).

The ImageChecker is a Python 3.8 module that accepts as an input a CSV file that containts 2 fields with N records and an output location where the processing results will be written to in csv format. 

Each of those fields contain the absolute path to an image file. The tool also provides the user with the ability to whitelist specific image types.


Even though the core developer & user workflow involves using the provided [Makefile](Makefile.md), ImageChecker can be executed in a few different ways wihout it:
* Running the python module locally
* Using a docker image containing the module and passing configuration & sample images as docker volumes
* Leverage a Kubernetes cluster and publish new images & configuration as configmaps. While this approach is not a best practice for handling images in a Kubernetes environment, it remains simple, with the only dependency being access to a Kubernetes clusters.

The following links provide detailed information for each topic:

* [Developer guide](docs/developer/README.md):
    * Python
    * Docker
    * Kubernetes
* [User guide](docs/user/README.md):

Contributing
------------

If you want to make any contributions, please follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so your changes get reviewed