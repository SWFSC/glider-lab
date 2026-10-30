---
name: ESD Slocum Glider Deployment
about: A comprehensive checklist for ESD glider deployments.
title: 'glider-YYYYmmdd deployment'
labels: ["Glider Build", "Data Management", "Data Processing"]
assignees: ''
---

A comprehensive checklist for ESD slocum glider deployments.

## Pre Deployment

### Glider Build
- [ ] Copy the template [deployment-prep folder](https://github.com/SWFSC/glider-lab/tree/main/deployment-prep/glider-YYYYmmdd-prep) in the [glider-lab repo deployment-prep folder](https://github.com/SWFSC/glider-lab/tree/main/deployment-prep) and rename it to 'glider-YYYYmmdd-prep', e.g. 'calanus-20241019-prep'. [Additional directions here](https://github.com/SWFSC/glider-lab/tree/main/deployment-prep#glider-deployment-prep-folder)
- [ ] Complete the [Glider Checkout Procedure](https://docs.google.com/document/d/1FdrB_BeSkKoy3XOzIwfmd_sm7aAwoaeT9AQfz0bkh8A/edit?usp=sharing)
- [ ] Update the Glider & Mooring Database with all relevant device and glider build information. This includes device calibration dates.
- [ ] Ensure all relevant calibration files are [uploaded](https://github.com/SWFSC/glider-lab/tree/main/calibration-docs) and check that you are using the most recent calibration values in autoexec.mi
- [ ] Coordinate and confirm sensor settings and sampling routine with PIs

### Data Prep
- [ ] Once the database is up-to-date, work with Sam or Kourtney to generate yaml files. Check them, and then commit them to the [glider-processing repo](https://github.com/SWFSC/glider-processing/tree/main/deployment-configs). Check project, acknowledgment, and PIs for IOOS [here](https://docs.google.com/spreadsheets/d/1Z-Lsijv_r0scLKnb5nPQiAadC218BnZy5bG4ajYFqcE/edit?usp=sharing). Specific checks:
    - [ ] Update the 'contributor_name' and 'contributor_role' blocks
    - [ ] deployment_name
    - [ ] 'summary': Use a previous summary as a template or work with Jen/team to write a new one
    - [ ] 'deployment_min_dt': This is the date/time that the glider disconnected from its initial.mi mission, and started its first 1k_n.mi mission. The format of this string must be 'YYYY-mm-dd HH:MM', e.g. "2025-04-14 18:45".
    - [ ] Confirm that the 'glider_devices' block contains correct and complete instrument info

## Deployment
- [ ] Pilots and boat crew coordinate and complete the [deployment procedure](https://docs.google.com/document/d/1uKzouLpEYnxL556pkscMwcALZTEX3Y5W0vupmwEt3lE/edit?tab=t.wqogdenk9spj)

## During Deployment

### Immediately after the deployment
- [ ] Update data folders with the official deployment name (glider-YYYYmmdd)
- [ ] Update the following blocks in the glider yaml file:
    - [ ] deployment_name
    - [ ] comment
    - [ ] summary
- [ ] Copy any new Cache files from SFMC to the [standard-glider-files](https://github.com/SWFSC/standard-glider-files/tree/main/Cache) cache folder
- [ ] Update the lab manual website deployments table (details TODO)

### Real Time Data Updates
- [ ] Routinely process real time data, publish to IOOS, and share results with PIs
- [ ] Share weekly updates in SWFSC Weekly Reports

## Post Deployment

- [ ] If necessary, do a final update of the glider yaml file in the glider-lab repo. The most common updates would be to the 'comment' block (e.g., if an instrument died during the deployment) or to the 'summary' block (e.g., one sentence summarizing the completed mission).

### Physical Glider Tasks
- [ ] After freshwater rinse, unplug all cables and connectors to dry out between deployments. Check for corrosion or damaged plugs/pins
- [ ] Recharge batteries for redeployment if applicable

### Data management

#### Glider
*NOTE: for all checklist items in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP glider deployments folder](https://console.cloud.google.com/storage/browser/amlr-gliders-deployments-dev).*
*NOTE: for sample `gcloud storage` upload commands, see [this doc](https://docs.google.com/document/d/1wWxq79JPuD5A92XTeH-FVJYA87qW2UlfEtKU1yxrSb8/edit?usp=sharing)*

##### GCP:
- [ ] If pulling the memory cards, zip the Flight and Science folders, and upload them to 'glider-YYYYmmdd/backup'. {todo: how do we want to handle backups when we don't pull cards}
- [ ] If the glider is not being opened, follow methods [here for high-speed data download](https://docs.google.com/document/d/10WD0RvmtD3B5yXnNhMeQiUxuK524cDntec29c57cEyI/edit?usp=sharing)
- [ ] Binary data: Upload all delayed binary data, compressed or uncompressed, to 'glider-YYYYmmdd/data/binary/delayed', upload from logs and sent logs folders.
- [ ] Cache files: Upload any new cache files to the [standard-glider-files Cache folder](https://github.com/SWFSC/standard-glider-files/tree/main/Cache)

##### SFMC:
- [ ] Archive the deployment on the SFMC (NOTE: coordinate with pilots before doing this)
- [ ] Download the Glider Folder Archive Tar Ball from the SFMC, and upload it (zipped) to 'glider-YYYYmmdd/backup'
- [ ] SFMC archive: Confirm that the 'glider-YYYYmmdd/archive-sfmc' has all of the files that are present in the 'archive' folder in the Glider Folder Archive Tar Ball. Upload files from the Tar Ball 'archive' folder to the GCP 'archive-sfmc' folder
- [ ] Download the Event Timeline: go to the event timeline page ('Options -> View Event Timeline'), and export ('Options -> Export Event Timeline'). Make sure the time range is for the full deployment, and download this file as 'glider-YYYYmmdd-event-timeline.xls'. Next, reformat the 'Time' column as "m/d/yyyy h:mm:ss", and save this file as a CSV ('glider-YYYYmmdd-event-timeline.csv') for long-term compatibility. Finally, upload the CSV to 'glider-YYYYmmdd/backup'

##### GitHub Prep Folder:
- [ ] Finalize any changes to the GitHub prep folder. Move the folder to the associated year folder to indicate that this deployment is no longer active

#### Active Acoustics
Acoustics tasks, if the glider was carrying an active acoustic instrument. These instructions apply to both AZFP and Nortek acoustics.

NOTE: in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP acoustics folder](https://console.cloud.google.com/storage/browser/amlr-gliders-acoustics-dev)

- [ ] Upload raw acoustic data to 'glider-YYYYmmdd/data/delayed'
- [ ] Upload acoustic config files to 'glider-YYYYmmdd/config'. These include any acoustic-related files from the 'archive-sfmc' folder

#### Passive Acoustics
Acoustics tasks, if the glider was carrying a passive acoustic instrument. These instructions apply to both WISPR and DMON acoustics.

- [ ] Upload raw acoustic data to PAM SI bucket (steps to-do)
- [ ] Upload acoustic config files to 'glider-YYYYmmdd/config'. These include any acoustic-related files from the 'archive-sfmc' folder
- [ ] Upload or link config files to PAM SI bucket (steps to-do)

#### Imagery
Imagery tasks, if the glider was carrying a camera. These instructions apply to both glidercam and shadowgraph imagery.

NOTE: in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP raw imagery folder](https://console.cloud.google.com/storage/browser/amlr-gliders-imagery-raw-dev)

- [ ] Upload imagery to 'glider-YYYYmmdd/images'
- [ ] Upload camera config files to 'glider-YYYYmmdd/config'. These include any imagery-related files from the 'archive-sfmc' folder and files from the camera (shadowgraph v2 - .cfg, shadograph v3 - .json)
- [ ] Work with Sam or Kourtney to 'refresh' VIAME-Web-AMLR, so that the images are visible through the VIAME-Web-AMLR platform.

## Data processing

### Base Glider Data Processing
- [ ] Update the Glider & Mooring Database with deployment information: deployment_end date, number of dives
- [ ] Follow [methods here](https://docs.google.com/document/d/14myLiV8ciZGOcj7Tjvvt_LmZjjTncJT7BC0FA8k1Bqw/edit?pli=1&tab=t.1wcx64hoeeta#heading=h.2hq1i54rgfs5) to complete delayed mode processing

### Glider Data Sharing and Archive
- [ ] Submit glider data files to IOOS NGDAC - [starter directions here](https://docs.google.com/document/d/14myLiV8ciZGOcj7Tjvvt_LmZjjTncJT7BC0FA8k1Bqw/edit?pli=1&tab=t.1wcx64hoeeta#heading=h.aqb7xl8xhy31)
- [ ] Update the lab manual website deployments table (details TODO)
- [ ] Complete [post-deployment report](https://github.com/SWFSC/glider-processing/tree/main/deployment-reports)

### Additional Sensor Data Processing

#### Active Acoustics
- [ ] Tasks TODO

#### Passive Acoustics
- [ ] Tasks TODO

#### Imagery
[Methods here](https://docs.google.com/document/d/14myLiV8ciZGOcj7Tjvvt_LmZjjTncJT7BC0FA8k1Bqw/edit?pli=1&tab=t.1wcx64hoeeta#heading=h.6ss8kwz8wos2)
- [ ] Create metadata files
- [ ] Generate JSON files for Optics SI processing
- [ ] Trigger OSI DAG runs
- [ ] Notify Andy and Jen when images are uploaded to VIAME and processing files are ready in the cloud
