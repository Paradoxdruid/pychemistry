# pychemistry
A collection of python scripts for chemistry and biochemistry

![gpl3.0](https://img.shields.io/github/license/Paradoxdruid/pychemistry.svg "GPL 3.0 Licensed")  [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Paradoxdruid/pychemistry.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Paradoxdruid/pychemistry/context:python)  [![CodeFactor](https://www.codefactor.io/repository/github/paradoxdruid/pychemistry/badge)](https://www.codefactor.io/repository/github/paradoxdruid/pychemistry) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) 


## Current Scripts

1. [buffer_app](#buffer_app)
2. [mol2scad](#mol2scad)
3. [dashmichaelis](#dashmichaelis)
4. [dashbuffers](#dashbuffers)

### buffer_app

`buffer_app` is a quick GUI (Tkinter or Qt) to quickly calculate recipes for stock buffer dilution and adjustment.

**Usage**

```
python buffer_app.py
```

![buffer_app screenshot](/images/buffer_app.png)

### mol2scad

`mol2scad` is a script to turn molecular coordinates into SCAD files.  Takes molfile / sdf coordinates as input, outputs a scad file for OpenSCAD.

See [mol2scad README](/scripts/mol2scad/README.md) for details.

### dashmichaelis

`dashmichaelis` is a Dash webapp for regression fitting of enzyme kinetics data to a Michaelis-Menten model.

**Usage**

This web app is hosted at [Michaelis.BonhamCode.com](https://michaelis.bonhamcode.com)

To activate it locally in a test environment:
```
python dashmichaelis.py
```

### dashbuffers

`dash-buffers` is a Dash webapp for biochemical buffer adjustment.

**Usage**

This web app is hosted at [Buffer.BonhamCode.com](https://buffer.bonhamcode.com)

To activate it locally in a test environment:
```
python dash-buffers.py
```


## Authors
These scripts are developed as academic software by [Dr. Andrew J. Bonham](https://github.com/Paradoxdruid) at the [Metropolitan State University of Denver](https://www.msudenver.edu). It is licensed under the GPL v3.0.
