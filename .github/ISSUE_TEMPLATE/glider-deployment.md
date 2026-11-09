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

## Metadata Prep

- [ ] Confirm the following pieces of glider metadata. These values will go in the deployment config yaml file:
    - [ ] deployment contributors, including PIs (or program leads), glider pilots, data managers
    - [ ] summary. Guidance: "Provide a useful summary or abstract for the data in the file. This summary is used as the primary piece of information describing the data set for discovery and archiving purposes. As such, careful thought should be put into constructing the summary."
    - [ ] funding acknowledgement. Specifically, does the acknowledgement need to be different than "This work was supported by funding from NOAA Fisheries, SWFSC."?

## Deployment
- [ ] Pilots and boat crew coordinate and complete the [deployment procedure](https://docs.google.com/document/d/1uKzouLpEYnxL556pkscMwcALZTEX3Y5W0vupmwEt3lE/edit?tab=t.wqogdenk9spj)

## During Deployment

### Immediately after the deployment
- [ ] Update data folders with the official deployment name (glider-YYYYmmdd)
- [ ] Copy any new Cache files from SFMC to the [standard-glider-files](https://github.com/SWFSC/standard-glider-files/tree/main/Cache) cache folder
- [ ] Update the lab manual website deployments table (details TODO)

### Metadata 
- [ ] Once the glider has been deployed and the database is up-to-date, generate the base yaml files using [generate-deployment-yaml.py](https://github.com/SWFSC/esdglider/blob/main/scripts/generate-deployment-yaml.py). Check them, and then commit them to the [glider-processing repo](https://github.com/SWFSC/glider-processing/tree/main/deployment-configs). In particular:
    - [ ] update acknowledgment, 'contributor_name', 'contributor_role', and summary with values from Metadata Prep
    - [ ] update 'deployment_name'
    - [ ] update 'comment': any miscellaneous info about the deployment or data set that is both relevant to data users and doesn't belong in 'summary'. 
    - [ ] update 'start_date': this is the date/time that the glider disconnected from its last test mission (historically od5.mi), and started its first real mission (historically 1k_n.mi). The format of this string must be 'YYYY-mm-dd HH:MM', e.g. "2025-04-14 18:45".
    - [ ] confirm that the 'glider_devices' block contains correct and complete instrument info
    - [ ] confirm 'sea_name': must be an [NCEI-approved value](https://www.ncei.noaa.gov/data/oceans/ncei/vocabulary/seanames.xml)

### Real Time Data Updates
- [ ] Routinely process real time data, publish to IOOS, and share results with PIs
- [ ] Share weekly updates in SWFSC Weekly Reports

## Post Deployment

- [ ] If necessary, do a final update of the glider yaml file in the glider-processing repo. The most common updates would be to the 'comment' block (e.g., if an instrument died during the deployment) or to the 'summary' block (e.g., one sentence summarizing the completed mission).

### Physical Glider Tasks
- [ ] After freshwater rinse, unplug all cables and connectors to dry out between deployments. Check for corrosion or damaged plugs/pins
- [ ] Recharge batteries for redeployment if applicable

### Data management

*NOTE: for all checklist items in this section, 'glider-YYYYmmdd' refers to the deployment name, e.g. amlr08-20220513*
*NOTE: ESD glider data transfer protocols, see [here](https://docs.google.com/document/d/15WY6TqTpKeD9eRm6Y2qny7714sRGbMqrtcnfTreQTlU/edit?usp=sharing)*

#### Glider

If the glider is not being opened, follow methods [here for high-speed data download](https://docs.google.com/document/d/10WD0RvmtD3B5yXnNhMeQiUxuK524cDntec29c57cEyI/edit?usp=sharing).

Glider data in bucket: [swfscesd-glider-deployments-data-in](https://console.cloud.google.com/storage/browser/swfscesd-glider-deployments-data-in)

Glider backup bucket: [swfscesd-glider-deployments-backup](https://console.cloud.google.com/storage/browser/swfscesd-glider-deployments-backup)

##### GCP:
- [ ] If the glider is not being opened, follow methods [here for high-speed data download](https://docs.google.com/document/d/10WD0RvmtD3B5yXnNhMeQiUxuK524cDntec29c57cEyI/edit?usp=sharing)
- [ ] Binary data: Upload all delayed binary data, compressed or uncompressed, to a 'delayed' folder in the 'data in' bucket: 'gs://swfscesd-glider-deployments-data-in/YYYY/glider-YYYYmmdd/binary/delayed'. 
- [ ] Backups: Upload backups of the full flight and science folders (zipped or unzipped) to a 'glider-files' folder in the 'backup' bucket: 'gs://swfscesd-glider-deployments-backup/YYYY/glider-YYYYmmdd/glider-files'
- [ ] Cache files: Upload any new cache files to the [standard-glider-files Cache folder](https://github.com/SWFSC/standard-glider-files/tree/main/Cache)

##### SFMC:
- [ ] Archive the deployment on the SFMC (NOTE: coordinate with pilots before doing this). Once archived:
    - [ ] Download the Glider Folder Archive Tar Ball from the SFMC, and upload it (zipped) to the 'backup' bucket: 'gs://swfscesd-glider-deployments-backup/YYYY/glider-YYYYmmdd'. Keep the original name of the zip file generated by the SFMC
- [ ] SFMC archive: Work with Sam or Kourtney to run the [sync-archive-from-sfmc.py](https://github.com/SWFSC/esdglider/blob/main/scripts/sync-archive-from-sfmc.py) script. Confirm that the 'glider-YYYYmmdd/archive-sfmc' has all of the files that are present in the 'archive' folder in the Glider Folder Archive Tar Ball. Alternatively, upload files from the Tar Ball 'archive' folder to the GCP 'archive-sfmc' folder
- [ ] Download the Event Timeline: go to the event timeline page ('Options -> View Event Timeline'), and export ('Options -> Export Event Timeline'). Make sure the time range is for the full deployment, and download this file as 'glider-YYYYmmdd-event-timeline.xls'. Next, reformat the 'Time' column as `"m/d/yyyy h:mm:ss"`, and save this file as a CSV ('glider-YYYYmmdd-event-timeline.csv') for long-term compatibility. Finally, upload the CSV to the 'backup' bucket, within: 'gs://swfscesd-glider-deployments-backup/YYYY/glider-YYYYmmdd'.

##### GitHub Prep Folder:
- [ ] Finalize any changes to the GitHub prep folder. Move the folder to the associated year folder to indicate that this deployment is no longer active

#### Active Acoustics
Acoustics tasks, if the glider was carrying an active acoustic instrument. These instructions apply to both AZFP and Nortek acoustics.

Active Acoustics data in bucket: [swfscesd-glider-active-acoustics-data-in](https://console.cloud.google.com/storage/browser/swfscesd-glider-active-acoustics-data-in)

- [ ] Upload raw acoustic data to 'gs://swfscesd-glider-active-acoustics-data-in/YYYY/glider-YYYYmmdd/data/delayed'
- [ ] Upload acoustic config files to 'gs://swfscesd-glider-active-acoustics-data-in/YYYY/glider-YYYYmmdd/config'. TBD if this includes all acoustic-related files from the 'archive-sfmc' folder

#### Passive Acoustics
Acoustics tasks, if the glider was carrying a passive acoustic instrument. These instructions apply to both WISPR and DMON acoustics.

Passive Acoustics data in bucket: todo

- [ ] Upload raw acoustic data to PAM SI bucket (steps to-do)
- [ ] Upload or link config files to PAM SI bucket (steps to-do)

#### Imagery
Imagery tasks, if the glider was carrying a camera. These instructions apply to both glidercam and shadowgraph imagery. Follow the [ESD glider data transfer protocols](https://docs.google.com/document/d/15WY6TqTpKeD9eRm6Y2qny7714sRGbMqrtcnfTreQTlU/edit?usp=sharing) to use rclone to avoid credential timeout errors. 

Glider imagery in bucket: [swfscesd-glider-imagery-data-in](https://console.cloud.google.com/storage/browser/swfscesd-glider-imagery-data-in)

- [ ] Upload imagery to the imagery in bucket. Specifically, upload all directory folders to a 'images' folder in the 'imagery in' bucket: 'gs://swfscesd-glider-imagery-data-in/YYYY/glider-YYYYmmdd/images'.
- [ ] ~~Upload camera config files to 'glider-YYYYmmdd/config'. These include any imagery-related files from the 'archive-sfmc' folder and files from the camera (shadowgraph v2 - .cfg, shadograph v3 - .json)~~
- [ ] Follow [this process](https://drive.google.com/file/d/18wzhSbPgsD59CY_3sJjddUeA-DbtSjP8/view?usp=drive_link) to 'refresh' VIAME-Web ESD, so that the images are visible through ESD's VIAME-Web deployment. 

## Data processing

### Base Glider Data Processing
*NOTE: If the glider is carrying a camera, imagery metadata files must be created before running the base processing*
- [ ] Unless the same glider is already back in the water, run the real-time script one last time, to catch all real-time data
- [ ] Follow [methods here](https://docs.google.com/document/d/14myLiV8ciZGOcj7Tjvvt_LmZjjTncJT7BC0FA8k1Bqw/edit?pli=1&tab=t.1wcx64hoeeta#heading=h.2hq1i54rgfs5) to complete delayed mode processing
- [ ] Update the Glider & Mooring Database with deployment information: deployment_end date, number of dives

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
- [ ] Trigger OSI DAG runs, and notify Andy
- [ ] Notify Andy and Jen when images are mirrored within VIAME, and processing files are ready in the cloud
