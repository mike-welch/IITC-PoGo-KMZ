# PoGoKMZ - Pokemon Go KMZ Generator

This repository contains code to store Pokemon Go data into a KMZ file that can be uploaded to [MyMaps](https://mymaps.google.com) for distribution within your local community.

## How to Use

The file `pogo-map.py` can be run directory from the command line and takes the name of your map as input:

```cmd
python pogo-map.py Your_Map_Name_Here
```

The script will automatically load the following files if they exist:

- `IITC-pogo.json`, an export from the PoGo Tools IITC plugin
- `sponspored.json`, a json file containing information for sponspored pokestops and gyms, the formating is consistent with data.json

## Requirements

Usage of this tool will require an Ingress account in order to access the [Ingress Intel Map](https://intel.ingress.com/intel) and the [PoGo Tools](https://gitlab.com/AlfonsoML/pogo-s2/) IITC plugin.

This code is developed in Python 3.7 and does not have any external dependencies.
