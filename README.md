# SUNZIP

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

---
![PyPI](https://img.shields.io/pypi/pyversions/sunzip.svg)
![Wheel](https://img.shields.io/pypi/wheel/sunzip.svg)
![Downloads](https://img.shields.io/pypi/dm/sunzip.svg)
![version](https://img.shields.io/pypi/v/sunzip.svg)
[![travis-ci](https://travis-ci.org/twbgc/sunzip.svg?branch=master)](https://travis-ci.org/twbgc/sunzip)
[![codecov](https://codecov.io/gh/twbgc/sunzip/branch/master/graph/badge.svg)](https://codecov.io/gh/twbgc/sunzip)

## Introduction

### Why are we doing this?

According to [Cara Marie](https://youtu.be/IXkX2ojrKZQ?t=331), an archive bomb a.k.a. A zip bomb is often employed to disable antivirus software, in order to create an opening for more traditional viruses. In addition, various kinds of pitfalls may occur during decompression.

### [Description for decompression pitfalls on zipfile doc](https://docs.python.org/3.8/library/zipfile.html)

### What is zip bomb?
It often appeared as a relatively small size zip file. And the unzipped file will be much larger than the zipped one.
This would probably cause a problem when your disk volume or memory is relatively small than the unzipped one.

### How do we defense zip bomb?

* Defense Layer 1 - checks perform on the server side.

```
    1. Check if it's a nested zip file. (i.e. 42.zip)
    2. Check if the compression ratio (Uncompressed Content/Compressed Content) 
       is greater than the threshold?
    3. Check if the file format is expected for context.
    4. Upload file size does not exceed the maximum limit. 
```

* Defense Layer 2 - limit the number of resources available to the process and its children.

```
    1. Check if CPU time is greater than the threshold.
    2. Check if the extracted part in memory is oversized. (memory usage)
```
  
* Defense Layer 3 - filetype-specific mitigations.

  Filetype: Archives
```
    1. Restrict output file size and number of extracted files 
       to ensure the total doesn't exceed the maximum limit.
```

### How do we set thresholds?

  ```
  Defense Layer 1:
    Uncompressed content size:  200 MB (vt)
    Compression ratio:          https://youtu.be/IXkX2ojrKZQ?t=553
  
  Defense Layer 2:
    CPU time:                   2 seconds(vt)
    Memoery oversized:
    
  Defense Layer 3:
    Output file size:
    Number of extracted files:
  ```

### Useful resources

  ```
  Bomb Codes
  https://bomb.codes/
  
  Mitigation Summary
  https://youtu.be/IXkX2ojrKZQ?t=1296
  
  Defense layers
  https://bomb.codes/mitigations
  ```


## Install


```bash
$ pip3 install sunzip
```

```bash
# for development use "development mode"
# https://packaging.python.org/tutorials/installing-packages/
$ pip3 install -e <directory to project root>
```


## Usage

```bash
# for command line usage see the help
$ sunzip-cli -h
```
You can find the arguments defined at the top of [cli.py](./sunzip/cli.py)

```python=
import sunzip

f = sunzip.Sunzip("archive.zip")
```


**Customize your resource limit.**

*Maximum compression ratio threshold*
```python=
f.threshold = 50
```
*Maximum CPU time (second)*
```python=
f.cpu = 1
```
*Maximum memory usage (byte)*
```python=
f.memory = 1024
```
*Maximum file size (byte)*
```python=
f.filesize = 1024
```

If there is no setting, the default value will be used.

`extract()` would perform a series of the above checks before decompression. If all pass, the zip file will be decompressed.

```python=
import sunzip

f = sunzip.Sunzip("archive.zip")

f.extract()
```
