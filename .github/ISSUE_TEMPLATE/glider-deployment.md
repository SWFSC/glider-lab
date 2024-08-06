---
name: ESD Glider Deployment
about: Checklist for tasks associated with each ESD glider deployment
title: glider-YYYYmmdd deployment
labels: ''
assignees: ''

---

Checklist for ESD glider deployment todo tasks. Note that file paths are relative to the top-level glider folder (i.e. glider-YYYYYmmdd)

# Before deployment

## Glider Build
- [ ] Determine what batteries will be used for the mission (primary or rechargeable) and install. This includes a new emergency battery. Write installation date on the primary batteries. Make sure the correct amphrs are in autoexec.mi (f_coulomb_battery_capacity). If using used primary batteries, make sure that the amphrs are set by typing put m_coulomb_amphr_total (used amphrs).
- [ ] Ballast the glider for the condtions that it will be deplyed in. [TWR ballast sheet] (https://datahost.webbresearch.com/download/file.php?id=91) [Rutgers ballast sheet] (https://docs.google.com/spreadsheets/d/1BrgEZyT4qzZ22Rkcxc7ZHFRZ-m1zfW3o/edit?usp=sharing&ouid=102683297276185841842&rtpof=true&sd=true)
- [ ] Check pump range while in the ballast tank if the glider hasn't been used in a while.
- [ ] Make sure the glider has the most recent operating system. [Datahost website](https://datahost.webbresearch.com/files.php?cwd=/glider)
- [ ] Final Seal. Replace all the hull seals and O-rings for sensors that need replacing. Note the internal and external weight distribution on the Ballast Sheet. As you seal the glider at each section, take photos of the connections.
- [ ] After Final Seal, recheck the ballast and that the roll is less than 5 degrees.
- [ ] Perform a Functional Checkout Procedure. Also download the longterm.sta
- [ ] Check on [Argos website] (https://argos-system.clsamerica.com/argos-cwi2/login.html) that the glider Argos test worked during the Functional Checkout Procedure.
- [ ] If possible, in the tech tank, perform the missions od5.mi and 1k_n.mi. Make sure the glider looks like it is diving close to correctly and that all the sensors are working and collecting data. 
- [ ] Make sure that the serial numbers are correct in autoexec.mi and proglets.dat and update [Fleet Status] (https://docs.google.com/spreadsheets/d/1tB3QNKYx8qOYYS9QZotekBAx0y-_n2d-EZPjFFdYNuU/edit?gid=0#gid=0)
- [ ] Create a glider build in the [glider database]  that has the correct serial numbers. You must be on the network or VPN to access the database.
## Glider Planning
- [ ] Planner provide, in one location, written sensor settings.[Settings and Sampling Document](https://docs.google.com/spreadsheets/d/1SNjvXY9RhGC8St3bXdfQx6tWN10sF8evctD0B_RcTKk/edit?gid=0#gid=0)
- [ ] Load all files and settings on the glider and attached sensors (ie Shadowgraph, AZFP, Nortek).
- [ ] If possible, verify sensor settings for camera, azfp, and/or Nortek. Either through a test file or some sensor dependent way. (ie silhouetteConfig.txt for camera, Getall comand for Nortek)
- [ ] Functional checkout procedure (FCP). Download autoexec.mi, proglets.dat, and all glider and science data from the FCP.
- [ ] Ballast glider in ballast tank to deployment condtions. 
- [ ] Test dive glider in Tech Tank using mission and sensor parameters. (OD5.mi and 1k_n.mi) All sensor output should be seen (ie .ad2, .azf, .cam)
- [ ] Put files on the SFMC to be loaded on the glider just before deployment. (mission and mission related (ma files), sensor cfg and ini, and sample files.

## Data prep
- [ ] Copy the [glider template folder](https://console.cloud.google.com/storage/browser/_details/amlr-gliders-deployments-dev/template-glider-YYYYmmdd.zip;tab=live_object?project=ggn-nmfs-usamlr-dev-7b99) into the correct project folder (FREEBYRD, REFOCUS, or SANDIEGO), and rename as applicable.
- [ ] Delete sensor folders (e.g., shadowgraph) if the glider does not have that specific sensor
- [ ] Add files to the 'deployment/docs/prep' folder as necessary. Include Functional Checkout folder along with config, ini, and ma files. Add Ballast sheet and Tech tank dive data if available.
- [ ] Add sealing photos to the 'deployment/docs/photos' folder.
- [ ] Add files to the ‘sensor/…/config’ folders as necessary. This includes Camera(solocam.cfg and solocam.ini), Nortek (ad2cp.cfg and ad2cp.ini), AZFP (azfp.cfg and azfp.ini)
- [ ] Update the [Glider&Mooring Database] (\\swc-storage4-s\AMLR_Datasets\Glider Database) with device and glider build information, making sure that the serial numbers are correct. 
- [ ] Copy default gdm config from [here](https://github.com/us-amlr/amlr-gliders/tree/main/resources/config-templates) into 'glider/config/gdm'. Edit deployment.yml, global_attributes.yml, and instruments.yml. In particular, update the instruments (names, serial numbers, and calibration dates) and the summary block in global_attributes.yml.

# During deployment

## Glider
- [ ] Day two of the deployment, download one set of sensor diagnostic data (ie .ad2, .azf, .cam) 

## Data prep
- [ ] Ensure the deployment folder name has the actual deployment date (e.g. amlr01-20220601)
- [ ] Ensure the deployment folder is in the glider deployments bucket ([amlr-gliders-deployments-dev](https://console.cloud.google.com/storage/browser/amlr-gliders-deployments-dev;tab=objects?project=ggn-nmfs-usamlr-dev-7b99))
- [ ] Update the Glider&Mooring Database with deployment information, and any last-minute changes

# After deployment
- [ ] Back up data: if applicable, put zipped copies of the Flight and Science folders in 'glider/backup'
- [ ] Populate the ‘glider/logs’ folder, either with a) all files from both sets of the LOGS and SENTLOGS folders (if doing a full download), or b) all of the files transferred over the air
- [ ] Copy the Cache files to [cache folder](https://console.cloud.google.com/storage/browser/amlr-gliders-deployments-dev/cache?project=ggn-nmfs-usamlr-dev-7b99) in the GCP bucket
- [ ] Copy all dbd and ebd files to ‘glider/data/in/binary/delayed
- [ ] Download desired comms (e.g., Event Timeline) from the SFMC to ‘docs/comms’
- [ ] If applicable, copy sensor config files to the various config directories in 'sensors'
- [ ] If applicable, copy AZFP data to ‘sensors/azfp/data/in/delayed’
- [ ] If applicable, copy glidercam data to the GCP [imagery bucket](https://console.cloud.google.com/storage/browser/amlr-imagery-raw-dev/gliders?project=ggn-nmfs-usamlr-dev-7b99)
- [ ] If applicable, copy Nortek data to ‘sensors/nortek/data/in/delayed’
- [ ] If applicable, copy shadowgraph images to the GCP [imagery bucket](https://console.cloud.google.com/storage/browser/amlr-imagery-raw-dev/gliders?project=ggn-nmfs-usamlr-dev-7b99)
- [ ] Update the Glider&Mooring Database with deployment information, and any last-minute changes

# Data processing
- [ ] Ensure that gdm config files at 'glider/config/gdm' are updated
- [ ] Run amlr_binary_to_dba.py script from amlr-gliders to convert binary data files to ascii (DBA) files
- [ ] Run amlr_process_dba_to_nc.py script from amlr-gliders with --write_trajectory flag to write trajectory NetCDF files
- [ ] If applicable, run amlr_process_dba_to_nc.py script from amlr-gliders with --write_acoustics and --write_imagery flags to write files for acoustic and imagery data processing
