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
- [ ] Ensure all relevant calibration files are [uploaded](https://github.com/SWFSC/glider-lab/tree/main/calibration-docs) and check that you are using the most recent calibration values in autoexec.mi
- TODO: how to coordinate with PIs for sensor settings and sampling?

## Metadata Prep

- [ ] Confirm the following pieces of glider metadata. These values will go in the deployment config yaml file:
    - [ ] deployment contributors, including PIs (or program leads), glider pilots, data managers
    - [ ] summary. Guidance: "Provide a useful summary or abstract for the data in the file. This summary is used as the primary piece of information describing the data set for discovery and archiving purposes. As such, careful thought should be put into constructing the summary."
    - [ ] funding acknowledgement. Does the acknowledgmeent need to be different than "This work was supported by funding from NOAA Fisheries, SWFSC."?


# During Deployment

## Immediately after the deployment
- [ ] Update the database and the data folders with the official deployment name (glider-YYYYmmdd)
- [ ] Copy any new Cache files to the [standard-glider-files](https://github.com/SWFSC/standard-glider-files/tree/main/Cache) Cache folder

### Metadata 
- [ ] Once the glider has been deployed and the database is up-to-date, generate the base yaml files using [generate-deployment-yaml.py](https://github.com/SWFSC/esdglider/blob/main/scripts/generate-deployment-yaml.py). Check them, and then commit them to the [glider-processing repo](https://github.com/SWFSC/glider-processing/tree/main/deployment-configs). In particular:
    - [ ] update acknowledgment, 'contributor_name', 'contributor_role', and summary with values from Metadata Prep
    - [ ] update 'deployment_name'
    - [ ] update 'comment': any miscellaneous info about the deployment or data set that is both relevant to data users and doesn't belong in 'summary'. 
    - [ ] update 'start_date': this is the date/time that the glider disconnected from its last test mission (historically od5.mi), and started its first real mission (historically 1k_n.mi). The format of this string must be 'YYYY-mm-dd HH:MM', e.g. "2025-04-14 18:45".
    - [ ] confirm that the 'glider_devices' block contains correct and complete instrument info
    - [ ] confirm 'sea_name': must be an [NCEI-approved value](https://www.ncei.noaa.gov/data/oceans/ncei/vocabulary/seanames.xml)

### Real-time data processing
- [ ] Set up real-time data processing (details TODO)

# Post Deployment

- [ ] If necessary, do a final update of the glider yaml file in the glider-lab repo. The most common updates would be to the 'comment' block (e.g., if an instrument failed during the deployment) or to the 'summary' block.
- [ ] {TODO} Physical glider tasks?

## Data management

For sample `gcloud storage` upload commands, see [this doc](https://docs.google.com/document/d/1wWxq79JPuD5A92XTeH-FVJYA87qW2UlfEtKU1yxrSb8/edit?usp=sharing). For sample `rclone` upload commands, see [this doc](https://docs.google.com/document/d/15WY6TqTpKeD9eRm6Y2qny7714sRGbMqrtcnfTreQTlU/edit?usp=sharing)

### Glider

Buckets:

- Glider data in bucket: [swfscesd-glider-deployments-data-in](https://console.cloud.google.com/storage/browser/swfscesd-glider-deployments-data-in)
- Glider backup bucket: [swfscesd-glider-deployments-backup](https://console.cloud.google.com/storage/browser/swfscesd-glider-deployments-backup)

NOTES: 

#### GCP:

- [ ] Binary data: Upload all delayed binary data, compressed or uncompressed, to a 'delayed' folder in the 'data in' bucket: 'gs://swfscesd-glider-deployments-data-in/YYYY/glider-YYYYmmdd/binary/delayed'. 
- [ ] Backups: Upload backups of the full flight and science folders (compressed or uncompressed) to a 'glider-files' folder in the 'backup' bucket: 'gs://swfscesd-glider-deployments-backup/YYYY/glider-YYYYmmdd/glider-files'.

#### SFMC:

- [ ] Download the Event Timeline: go to the event timeline page ('Options -> View Event Timeline'), and export ('Options -> Export Event Timeline'). Make sure the time range is for the full deployment, and download this file as 'glider-YYYYmmdd-event-timeline.xls'. Next, reformat the 'Time' column as `"m/d/yyyy h:mm:ss"`, and save this file as a CSV ('glider-YYYYmmdd-event-timeline.csv') for long-term compatibility. Finally, upload the CSV to the 'backup' bucket: 'gs://swfscesd-glider-deployments-backup/YYYY/glider-YYYYmmdd'.
- [ ] Archive the deployment on the SFMC (NOTE: coordinate with Jen before doing this). Once archived: 
    - [ ] Download the Glider Folder Archive Tar Ball from the SFMC, and upload it (zipped) to the 'backup' bucket: 'gs://swfscesd-glider-deployments-backup/YYYY/glider-YYYYmmdd'.
    - [ ] Confirm that the 'archive-sfmc' folder in the 'data in' bucket ('gs://swfscesd-glider-deployments-data-in/YYYY/glider-YYYYmmdd/archive-sfmc') has all of the files that are present in the 'archive' folder in the Glider Folder Archive Tar Ball. Upload files from the Tar Ball 'archive' folder to the GCP 'archive-sfmc' folder as necessary. 

#### Data prep:

- [ ] Finalize any changes to the data prep folder. This folder does not need to go to GCP. 

### Active Acoustics

Acoustics tasks, if the glider was carrying an active acoustic instrument. These instructions apply to both AZFP and Nortek acoustics. 

SMW TODO

NOTE: in this section, 'glider-YYYYmmdd' refers to the deployment folder within the [GCP acoustics folder](https://console.cloud.google.com/storage/browser/amlr-gliders-acoustics-dev)

- [ ] Upload raw acoustic data to 'glider-YYYYmmdd/data/delayed'
- [ ] Upload acoustic config files to 'glider-YYYYmmdd/config'. These include any acoustic-related files from the 'archive-sfmc' folder

### Passive Acoustics

Acoustics tasks, if the glider was carrying a passive acoustic instrument. These instructions apply to both WISPR and DMON acoustics. 

- [ ] Upload raw acoustic data to PAM SI bucket (steps to-do)
- [ ] Upload acoustic config files to 'glider-YYYYmmdd/config'. These include any acoustic-related files from the 'archive-sfmc' folder
- [ ] Upload or link config files to PAM SI bucket (steps to-do)

### Imagery

Imagery tasks, if the glider was carrying a camera. These instructions apply to both glidercam and shadowgraph imagery. Follow the [ESD glider data transfer protocols](https://docs.google.com/document/d/15WY6TqTpKeD9eRm6Y2qny7714sRGbMqrtcnfTreQTlU/edit?usp=sharing) to use rclone to avoid credential timeout errors. 

- Glider imagery in bucket: [swfscesd-glider-imagery-data-in](https://console.cloud.google.com/storage/browser/swfscesd-glider-imagery-data-in)

- [ ] Upload imagery to the imagery in bucket. Specifically, upload all directory folders to a 'images' folder in the 'imagery in' bucket: 'gs://swfscesd-glider-imagery-data-in/YYYY/glider-YYYYmmdd/images'.
- [ ] ~~Upload camera config files to 'glider-YYYYmmdd/config'. These include any imagery-related files from the 'archive-sfmc' folder and files from the camera (shadowgraph v2 - .cfg, shadograph v3 - .json)~~
- [ ] Follow [this process](https://drive.google.com/file/d/18wzhSbPgsD59CY_3sJjddUeA-DbtSjP8/view?usp=drive_link) to 'refresh' VIAME-Web ESD, so that the images are visible through ESD's VIAME-Web deployment. 

## Data processing

- [ ] Base glider data processing: follow [these instructions](https://docs.google.com/document/d/14myLiV8ciZGOcj7Tjvvt_LmZjjTncJT7BC0FA8k1Bqw/edit?pli=1&tab=t.1wcx64hoeeta)
- [ ] Submit glider data files to IOOS NGDAC (see above doc)
- [ ] Update the Glider & Mooring Database with deployment information: proper deployment end date, number of dives
- [ ] Update the lab manual website deployments table (details TODO)
- [ ] Complete [post-deployment report](https://github.com/SWFSC/glider-processing/tree/main/deployment-reports)
