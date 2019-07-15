# pychemistry
A collection of python scripts for chemistry and biochemistry

![gpl3.0](https://img.shields.io/github/license/Paradoxdruid/pychemistry.svg "GPL 3.0 Licensed")  [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Paradoxdruid/pychemistry.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Paradoxdruid/pychemistry/context:python)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) 


## Current Scripts

1. [buffer_app.py](#buffer_apppy)
2. [mol2scad.py](#mol2scadpy)

### buffer_app.py

`buffer_app.py` is a quick GUI (Tkinter or Qt) to quickly calculate recipes for stock buffer dilution and adjustment.

**Usage**

```
buffer_app.py
```

### mol2scad.py

`mol2scad.py` is a script to turn molecular coordinates into SCAD files.  Takes molfile / sdf coordinates as input, outputs a scad file for OpenSCAD.

**Usage**

```
mol2scad.py -i <input molfile> -o <output scadfile>
```

## Authors
These scripts are developed as academic software by [Dr. Andrew J. Bonham](https://github.com/Paradoxdruid) at the [Metropolitan State University of Denver](https://www.msudenver.edu). It is licensed under the GPL v3.0.
