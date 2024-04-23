
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/hdfgroup/hsds_examples)



# HSDS (Highly Scalable Data Service) Example Programs

## Introduction
 
HSDS is a web service that implements a REST-based web service for HDF5 data stores.

This repository contains sample programs (mostly in Python) that demonstrate
utilizing this service.

All of the sample programs can be run in a Web browser without installing any software. 
To this end, this repository comes with a prebuild __[GitHub Codespaces](https://github.com/features/codespaces)__ configuration. Launch a Codespaces environment by clicking the banner __["Open in GitHub Codespaces"](https://codespaces.new/SEEKCommons/WorkshopTraining)__ and start evaluating the Jupyter notebooks (by placing the cursor into a code cell and pressing `Ctrl+Enter` or `Shift+Enter`). When prompted for a Python kernel, select
```
Python 3.10.13 ~/python/current/bin/python3
```

Alternatively, you can connect to the codespace environment using VS Code.  From VS Code, select the
command palette (Ctrl+Shift+P), and search for "Codespaces: Create New Codespace".

In either case, when the Codespace starts it will be running an HSDS instance and your environment will be automatically setup to connect to it.


It's also possible to run the examples locally on your desktop or EC2 instance.  In this case you'll need to setup an HSDS instance and configure your environment to connect to it.  See: https://github.com/HDFGroup/hsds/blob/master/README.md for instructions. 

The Python examples use the h5pyd package which provides a h5py-api compatible interface to the HSDS
REST API.  There are also examples, the explore using the REST API directly.
 
 
## Using the HSDS CLI (Command Line Interface) Tools

Once the above setup is complete, you can use the CLI tools to interact with the service.  To get help on a particular tool, run with the --help option.

The following tools are provided:

* hsconfigure -- setup credentials file
* hsinfo -- display status of HSDS service
* hsls -- list files in folders or contents of an HSDS domain
* hstouch -- create new folders or domains
* hsload -- upload a HDF5 file on your system to the server
* hsget -- download a file from the server to your computer
* hsdiff -- compare a HSDS domain with and HDF5 file
* hsstat -- get detailed information about a HSDS domain
* hsrm -- delete a domain or folder
* hsacl -- display or modify Access Control Lists (ACLs) for a domain or folder

## Using the Python SDK (h5pyd)

The Python SDK allows you to write Python programs using a package that shares the 
high-level API of the popular h5py package for regular HDF5 files.  See http://docs.h5py.org/en/latest/ for documentation of the API.

Notable differences:

* Since there's no concept of a current working directory, always provide an absolute path when opening a domain
* There is no explicit support for Parallel HDF5 or SWMR
* Some types are not yet supported: Object and Region references, Opaque
* h5pyd extends the Dataset class with a query method - see the ghcn_query example for usage

Many of the example programs can be run with either h5py or h5pyd.

## Running the notebook examples

To execute the notebook examples (extension .ipynb), click on a cell and press the arrow (or ctrl-enter)

## Additional Information

### Websites

* Main website: http://www.hdfgroup.org
* h5pyd: https://github.com/HDFGroup/h5pyd
* HSDS: https://github.com/HDFGroup/hsds
* Mailing list: hdf-forum@lists.hdfgroup.org <hdf-forum@lists.hdfgroup.org>

### Other useful resources

* RESTful HDF5 White Paper: https://www.hdfgroup.org/pubs/papers/RESTful_HDF5.pdf  
* SciPy17 Presentation: http://s3.amazonaws.com/hdfgroup/docs/hdf_data_services_scipy2017.pdf 
* HDF5 For the Web: https://hdfgroup.org/wp/2015/04/hdf5-for-the-web-hdf-server
* HSDS Security: https://hdfgroup.org/wp/2015/12/serve-protect-web-security-hdf5 


## Reporting bugs (and general feedback)

For problems with samples in this repository, create a new issue here: https://github.com/HDFGroup/hsds_examples/issues. 

For h5pyd-related problems, create new issues at http://github.com/HDFGroup/h5pyd/issues. 

For problems with the service itself, or general questions/feedback, please use the hdf list (hdf-forum@lists.hdfgroup.org) or contact the HDF help desk: help@hdfgroup.org



