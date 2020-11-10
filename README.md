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

## TCGA API Reference

### Download single file
```python
from gdcapiwrapper.tcga import Data
Data.download(uuid="uuid-file-you-wanna-download", path="/local/path", name="filename")
```
NOTE: `path` and `name` are optional, by default path is your current directory and if name is 
not provided it will be saved with the UUID as filname.

### Download multiple files
```python
from gdcapiwrapper.tcga import Data
response, filename =Data.download_multiple(uuid_list=["UUID1", "UUID2", "UUID3"], path="/local/path")
```
NOTE: `path` is optional, by default path is your current directory.


## TCIA API Reference

### Get a list of SOPInstanceUID for a given series
```python
from gdcapiwrapper.tcia import Data
# Example for CSV, HTML, XML
response, filename = Data.sop_instance_uids(
                        series_instance_uid="uid.series.instance",
                        format_="JSON",
                        path="/local/path", 
                        name="filename"
                    )
# Example for JSON
response, json = Data.sop_instance_uids(series_instance_uid="uid.series.instance")
```
Formats allowed: `["CSV", "HTML", "JSON", "XML"]`, default: `JSON`. When `JSON` is requested the API will not save any
json file on disk, returns an in memory json object.
 
NOTE: `path` and `name` are optional, by default path is your current directory and if name is 
not provided it will be saved with the SeriesInstance as filename.

### Download Single DICOM image
```python
from gdcapiwrapper.tcia import Data
response, filename = Data.download_single_image(
                        series_instance_uid="uid.series.instance",
                        sop_instance_uid="uid.sop.instance",
                        path="/local/path",
                        name="filename.dcm",
                    )
```
NOTE: `path` and `name` are optional, by default path is your current directory and if name is 
not provided it will be saved with the SOPInstanceUID as filename.

### Download set of images in a zip file 
```python
from gdcapiwrapper.tcia import Data
response, filename = Data.download_series_instance_images(
                        series_instance_uid="uid.series.instance",
                        path="/local/path",
                        name="filename.zip")
```
NOTE: `path` and `name` are optional, by default path is your current directory and if name is 
not provided it will be saved with the SOPInstanceUID as filename.