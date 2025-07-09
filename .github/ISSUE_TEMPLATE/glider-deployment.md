---
name: ESD Slocum Glider Deployment
about: A comprehensive checklist for ESD glider deployments.
title: glider-YYYYmmdd deployment
labels: ''
assignees: ''
---

A comprehensive checklist for ESD slocum glider deployments.

# Pre Deployment

## Glider Build
- [ ] Make a copy of the [GDrive folder template](https://drive.google.com/drive/folders/1xBYTSP8GOHA35bxVoqH7czrJn4ekYrjI?usp=drive_link) in the [Glider Deployment](https://drive.google.com/drive/folders/1qfKMxXH0hUhbmOp8aESidz-YO3IPxWM3?usp=sharing) Google Drive folder. Rename the template copy to 'glider-YYYYmmdd-prep', e.g. 'calanus-20241019-prep'.
- [ ] Complete the [Glider Checkout Procedure](https://docs.google.com/document/d/1FdrB_BeSkKoy3XOzIwfmd_sm7aAwoaeT9AQfz0bkh8A/edit?usp=sharing)
- [ ] Update the Glider & Mooring Database with all relevant device and glider build information. This includes device calibration dates.
- [ ] Ensure all relevant calibration files are [uploaded](https://github.com/SWFSC/glider-lab/tree/main/calibration-docs)
- TODO: how to coordinate with PIs for sensor settings and sampling? Revitalize [this sheet](https://docs.google.com/spreadsheets/d/1SNjvXY9RhGC8St3bXdfQx6tWN10sF8evctD0B_RcTKk/edit?usp=sharing)?

## Data Prep
- [ ] Once the database is up-to-date, work with Sam to generate yaml files. Check them, and then commit them to the [glider-lab repo](https://github.com/SWFSC/glider-lab/tree/main/deployment-configs). Specific checks:
    - [ ] Update the 'contributor_name' and 'contributor_role' blocks
    - [ ] deployment_name
    - [ ] 'summary': 
    - [ ] 'deployment_min_dt': This is the date/time that the glider disconnected from its last od5.mi mission, and started its first 1k_n.mi mission. The format of this string must be 'YYYY-mm-dd HH:MM', e.g. "2025-04-14 18:45".
    - [ ] Confirm that the 'glider_devices' block contains correct and complete instrument info

# During Deployment

## Immediately after the deployment
- [ ] Update data folders with the official deployment name (glider-YYYYmmdd)
- [ ] Update the following blocks in the glider yaml file:
    - [ ] deployment_name
    - [ ] comment
    - [ ] summary
- [ ] Copy any new Cache files to the [standard-glider-files](https://github.com/SWFSC/standard-glider-files/tree/main/Cache) cache folder
- [ ] Update the lab manual website deployments table (details TODO)
- [ ] Set up real-time data processing (details TODO)

# Post Deployment

- [ ] If necessary, do a final update of the glider yaml file in the glider-lab repo. The most common updates would be to the 'comment' block (e.g., if an instrument died during the deployment) or to the 'summary' block (e.g., one sentence summarizing the completed mission).
- [ ] {TODO} Physical glider tasks?

## Data management

If desired, see the [Template](https://drive.google.com/drive/folders/10QGrMjwwr5uZ-AISQtSBo0Hsm2zGnq0i?usp=drive_link) folder for template GCP directory structures

### Glider

NOTE: for all checklist items in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP glider deployments folder](https://console.cloud.google.com/storage/browser/amlr-gliders-deployments-dev).

NOTE: for sample `gcloud storage` upload commands, see [this doc](https://docs.google.com/document/d/1wWxq79JPuD5A92XTeH-FVJYA87qW2UlfEtKU1yxrSb8/edit?usp=sharing)

GCP:

- [ ] If pulling the memory cards, zip the Flight and Science folders, and upload them to 'glider-YYYYmmdd/backup'. If transferring files over the air, {todo}
- [ ] {todo: something special for log files?}
- [ ] Binary data: Upload all delayed binary data, compressed or uncompressed, to 'glider-YYYYmmdd/data/binary/delayed'

SFMC:

- [ ] Archive the deployment on the SFMC (NOTE: coordinate with Jen before doing this)
- [ ] Download the Glider Folder Archive Tar Ball from the SFMC, and upload it (zipped) to 'glider-YYYYmmdd/backup'
- [ ] SFMC archive: Confirm that the 'glider-YYYYmmdd/archive-sfmc' has all of the files that are present in the 'archive' folder in the Glider Folder Archive Tar Ball. Upload files from the Tar Ball 'archive' folder to the GCP 'archive-sfmc' folder as necessary
- [ ] Download the Event Timeline: go to the event timeline page ('Options -> View Event Timeline'), and export ('Options -> Export Event Timeline'). Make sure the time range is for the full deployment, and download this file as 'glider-YYYYmmdd-event-timeline.xls'. Next, reformat the 'Time' column as `"m/d/yyyy h:mm:ss"`, and save this file as a CSV ('glider-YYYYmmdd-event-timeline.csv') for long-term compatibility. Finally, upload the CSV to 'glider-YYYYmmdd/backup'

Google Drive:

- [ ] Finalize any changes to the Google Drive folder. Leave this folder in Drive - it does not need to go to GCP

### Acoustics

Acoustics tasks, if the glider was carrying an acoustic instrument. These instructions apply to both AZFP and Nortek acoustics. 

NOTE: in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP acoustics folder](https://console.cloud.google.com/storage/browser/amlr-gliders-acoustics-dev)

- [ ] Upload raw acoustic data to 'glider-YYYYmmdd/data/delayed'
- [ ] Upload acoustic config files to 'glider-YYYYmmdd/config'. These include any acoustic-related files from the 'archive-sfmc' folder

### Imagery

Imagery tasks, if the glider was carrying a camera. These instructions apply to both glidercam and shadowgraph imagery. 

NOTE: in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP raw imagery folder](https://console.cloud.google.com/storage/browser/amlr-gliders-imagery-raw-dev)

- [ ] Upload imagery to 'glider-YYYYmmdd/images'
- [ ] Upload camera config files to 'glider-YYYYmmdd/config'. These include any imagery-related files from the 'archive-sfmc' folder
- [ ] Work with Sam to 'refresh' VIAME-Web-AMLR, so that the images are visible through the VIAME-Web-AMLR platform.

## Data processing

- [ ] Base glider data processing
    - Details TODO
- [ ] Submit glider data files to IOOS NGDAC
- [ ] Update the Glider & Mooring Database with deployment information: deployment_end date, number of dives
- [ ] Update the lab manual website deployments table (details TODO)
- [ ] Complete [post-deployment report](https://github.com/SWFSC/glider-lab/tree/main/deployment-reports)
