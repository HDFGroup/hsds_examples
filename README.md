# HSDS (Highly Scalable Data Service) Example Programs

## Introduction
 
HSDS is a web service that implements a REST-based web service for HDF5 data stores.

This repository contains sample programs (mostly in Python) that demonstrate
utilizing this service.

## Setup
 
### Get Code

Clone this repository::

    $ git clone https://github.com/HDFGroup/hdfcloud_workshop

If you don't have git installed, you can get it here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### Install Python if you don't have it already

Python version 2.7 to 3.6 is fine. Check your version using::

    $ python --version

If you don't have Python installed, go to: https://www.python.org/downloads/.

### Install Pip if you don't have it already

Run::

   $ pip --version

If you don't have pip, get the installer srcript::

  $ wget https://bootstrap.pypa.io/get-pip.py

Then run the script::

   $ python get-pip.py 

If you run into problems, see: https://pip.pypa.io/en/stable/installing/.

### Install the necessary packages

Run::

   $ pip install h5pyd
   $ pip install h5py
   $ pip install jason
   $ pip install jupyter

Or if you are using Anaconda::

   $ conda create -n hsds python=3.6 h5py json jupyter
   $ source activate hsds
   $ pip install h5pyd

### Configure h5pyd
 
User credentials are stored in a .hscfg file in your home directory.
Contact The HDF Group to get your credentials (username and password).

Then run::

  $ hsconfigure

As prompted, enter the service endpoint, username, and password.

Verify that you can connect to the service::

  $ hsinfo

A folder in the path: "/home/<username>" should be setup with permissions for 
your account to create sub-folders and files within the folder.  

You can verify this with::

  $ hsls /home/<username>/  # list your home folder
  $ hstouch /home/<username>/empty.h5  # create a HDF5 domain (file)

## Using the HSDS CLI (Command Line Interface) Tools

Once the above setup is complete, you can use the CLI tools to interact with the service.  To get help on a particular tool, run with the --help option.

The following tools are provided:

* hsconfigure -- setup credentials file
* hsinfo -- display status of HSDS service
* hsls -- list files in folders or contents of an HDF5 file
* hstouch -- create new folders or files
* hsload -- upload a HDF5 file on your system to the server
* hsget -- download a file from the server to your computer
* hsdel -- delete a file or folder
* hsacl -- display or modify Access Control Lists (ACLs) for a file or folder

## Using the Python SDK (h5pyd)

The Python SDK allows you to write Python programs using a package that shares the 
high-level API of the popular h5py package for regular HDF5 files.  See http://docs.h5py.org/en/latest/ for documentation of the API.

Notable differences:

* Since there's no concept of a current working directory, always provide an absolute path when opening a file
* There is no explicit support for Parallel HDF5 or SWMR
* Some types are not yet supported: Object and Region references, Opaque
* Dimension Scales or not yet supported
* h5pyd extends the Dataset class with a query method - see the ghcn_query example for usage

## Running the notebook examples

Samples that have a notebook sub-directory contain one or more Jupyter notebooks.
To run, cd to that directory and type::

  $ jupyter notebook

This will open a browser window that will let you step through the notebook.

## Websites

* Main website: http://www.hdfgroup.org
* h5pyd Source code: https://github.com/HDFGroup/h5pyd
* Mailing list: hdf-forum@lists.hdfgroup.org <hdf-forum@lists.hdfgroup.org>
* Documentation: http://h5serv.readthedocs.org  (For REST API)

## Other useful resources

* RESTful HDF5 White Paper: https://www.hdfgroup.org/pubs/papers/RESTful_HDF5.pdf  
* SciPy17 Presentation: http://s3.amazonaws.com/hdfgroup/docs/hdf_data_services_scipy2017.pdf 
* HDF5 For the Web: https://hdfgroup.org/wp/2015/04/hdf5-for-the-web-hdf-server
* HSDS Security: https://hdfgroup.org/wp/2015/12/serve-protect-web-security-hdf5 


## Reporting bugs (and general feedback)

For h5pyd-related problems, create new issues at http://github.com/HDFGroup/h5pyd/issues. 

For problems with the service itself, or general questions/feedback, please use the hdf list (hdf-forum@lists.hdfgroup.org) or contact the HDF help desk: help@hdfgroup.org



