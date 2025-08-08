# glider-lab

Repository of the Ecosystem Science Division (ESD) glider lab at the Southwest Fisheries Science Center (SWFSC).

See the [glider lab manual](https://swfsc.github.io/glider-lab-manual) for more in-depth info.

## Directories

### GIS_layers

description todo

### calibration-docs

The calibration documents for the various ESD glider instruments. Within this folder, documents are grouped by instrument.

### deployment-configs

Deployment config files, for each deployment. These yaml files are used during data processing by [pyglider](https://github.com/c-proof/pyglider) and [glider-utils](https://github.com/SWFSC/esdglider). These files are typically created by first using [esdglider.config.make_deployment_config](https://github.com/SWFSC/esdglider/blob/main/esdglider/config.py) to make a file with the basic info, and then editing that file (e.g., adding the comment and summary blocks) by hand.

### deployment-reports

ESD glider deployment reports, created as Quarto documents. See the readme in this folder for more details.

### deployment-scripts

Scripts used for processing data from glider deployments. Typically, these scripts are meant to be run in GCP to a) create netCDF files from the delayed binary data after a glider has been recovered, and b) apply any corrections before sending the data to the NGDAC.

### echoview-glider-calib-files

Calibration files used by Tony when processing glider acoustic data using Echoview.

## Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
