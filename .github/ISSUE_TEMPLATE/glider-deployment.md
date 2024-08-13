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
- [ ] Determine what batteries will be used for the mission (Lithium primary or rechargeable) and install. This includes a new emergency battery. Write installation date on the primary batteries. Make sure the correct amphrs are in autoexec.mi (f_coulomb_battery_capacity). If using used primary batteries, make sure that the amphrs are set by typing put m_coulomb_amphr_total (used amphrs).
- [ ] Ballast the glider for the condtions that it will be deployed in. [TWR ballast sheet](https://datahost.webbresearch.com/download/file.php?id=91) or [Rutgers ballast sheet](https://docs.google.com/spreadsheets/d/1BrgEZyT4qzZ22Rkcxc7ZHFRZ-m1zfW3o/edit?usp=sharing&ouid=102683297276185841842&rtpof=true&sd=true)
- [ ] Optional. Check pump range while in the ballast tank if the glider hasn't been used in a while.
- [ ] Make sure the glider has the most recent operating system. [Datahost website](https://datahost.webbresearch.com/files.php?cwd=/glider)
- [ ] Final Seal. Replace all the hull seals and O-rings for sensors that need replacing. Note the internal and external weight distribution on the Ballast Sheet. As you seal the glider at each section, take photos of the connections.
- [ ] After Final Seal, recheck the ballast and that the roll is less than 5 degrees.
- [ ] Perform a Functional Checkout Procedure. Also download the longterm.sta when downloading the files that the Functional Checkout states. 
- [ ] Check on [Argos website](https://argos-system.clsamerica.com/argos-cwi2/login.html) that the glider Argos test worked during the Functional Checkout Procedure.
- [ ] If possible, in the tech tank, perform the missions od5.mi and 1k_n.mi using mission and sensor parameters. Make sure the glider looks like it is diving close to correctly and that all the sensors are working and collecting data. All sensor output should be seen including .ad2, .azf, .cam when applicable. 
- [ ] Make sure that the serial numbers are correct in autoexec.mi and proglets.dat and update [Fleet Status](https://docs.google.com/spreadsheets/d/1tB3QNKYx8qOYYS9QZotekBAx0y-_n2d-EZPjFFdYNuU/edit?gid=0#gid=0)
- [ ] Optional. Perform a compass calibration if necessary. [SOP](https://docs.google.com/document/d/1Ny_K8jxSWA71vFyzvtJ7bK2i5aDPo2gu/edit?usp=sharing&ouid=102683297276185841842&rtpof=true&sd=true)
- [ ] Calibrate Shadowgraph if installed. Then clear the memory if there were photos on it.
- [ ] Calibrate acoustics (AZFP or Nortek mini) if installed. Then clear the memory if data is on it.
## Glider Planning
- [ ] Planner provide, in one location, written sensor settings. [Settings and Sampling Document](https://docs.google.com/spreadsheets/d/1SNjvXY9RhGC8St3bXdfQx6tWN10sF8evctD0B_RcTKk/edit?gid=0#gid=0)
- [ ] Load all files and settings on the glider and attached sensors (ie Shadowgraph, AZFP, Nortek).
- [ ] If possible, verify sensor settings for camera, azfp, and/or Nortek. Either through a test file or some sensor dependent way. (ie silhouetteConfig.txt for camera, Getall comand for Nortek)
- [ ] Put files on the [SFMC](https://sfmc.webbresearch.com/sfmc/login) in the to-glider and to-science folders to be loaded on the glider just before deployment. (mission and mission related (ma files), sensor cfg and ini, and sample files.

## Data Prep
- [ ] Download the [GDrive folder template](https://drive.google.com/drive/folders/1xBYTSP8GOHA35bxVoqH7czrJn4ekYrjI?usp=drive_link) and rename it (glidername-YYYYmmdd). Then upload to [Glider Deployment](https://drive.google.com/drive/folders/1qfKMxXH0hUhbmOp8aESidz-YO3IPxWM3?usp=sharing) Google Drive.
- [ ] Download the [GCP folder template](https://drive.google.com/drive/folders/155F-NTGW-GGFyxpiUcZ3pAgqXG6h9vG3?usp=drive_link) and rename it (glidername-YYYYmmdd).
- [ ] Update the [Glider & Mooring Database](\\swc-storage4-s\AMLR_Datasets\Glider Database) with device and glider build information, making sure that the serial numbers are correct. 
