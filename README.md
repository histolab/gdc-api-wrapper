Genomic Data Commons API wrapper
================================
A simple Python wrapper for the [GDC Application Programming Interface (API)](https://portal.gdc.cancer.gov/)

[![Build Status](https://travis-ci.com/histolab/gdc-api-wrapper.svg?branch=master)](https://travis-ci.com/histolab/gdc-api-wrapper)
[![Coverage Status](https://coveralls.io/repos/github/histolab/gdc-api-wrapper/badge.svg?branch=master)](https://coveralls.io/github/histolab/gdc-api-wrapper?branch=master)

The GDC API drives the GDC Data and Submission Portals and provides programmatic access to GDC functionality. This includes searching for, downloading, and submitting data and metadata.

## Features implemented
- Downloading a Single File using GET 
- Downloading Multiple Files using POST

## Usage

### Installation
`pip install gdc-api-wrapper`

### Download single file
```python
from gdcapiwrapper.data import Data
Data.download(uuid="uuid-file-you-wanna-download", path="/local/path", name="filename")
```
NOTE: `path` and `name` are optional, by default path is your current directory and if name is 
not provided it will be saved with the UUID as filname.

### Download multiple files
```python
from gdcapiwrapper.data import Data
Data.download_multiple(uuid_list=["UUID1", "UUID2", "UUID3"], path="/local/path")
```
NOTE: `path` is optional, by default path is your current directory.
