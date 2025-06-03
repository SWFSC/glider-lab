README for glider report template

1. Make a copy of REPORT_TEMPLATE in C:\GitHub\glider-lab\deployment-reports
2. Rename REPORT_TEMPLATE.qmd with the glider deployment name (e.g., risso-20250414)
3. From GCP, download the deployment data from amlr-gliders-deployments-dev bucket (e.g., gs://amlr-gliders-deployments-dev/SANDIEGO/2025/risso-20250414) and place in C:\glider-lab\deployment-reports\Data
4. From the SFMC, download the archive folder from the glider terminal page
5. Rename the folder "file-archive" and place in the Data folder in Step 3
6. In the .qmd document, fill in glider name and deployment date on line 5
7. In first code chunk, change the following information:
	a. deployment<-"deployment name"
	b. comment in the correct locale ("CCE" for CA deployments and "Antarctica" for Antarctic deployments
	c. comment in correct battery configuration, comment out other configurations
	d. comment in sensor.file and sensor.spec objects for the sensors deployed on the glider (e.g., for the CTD, make sure "ctd.file" and "ctd.spec" are commented in. If the glider did not have an azfp, comment out azfp.file and azfp.spec)
	e. comment in appropriate "state.to.sample.xx" objects (may be more than one depending on how individual sensors were programmed)
	f. change "sample.depth" as necessary
8. Ensure "base.path" is set to the "Data" folder (C:\glider-lab\deployment-reports\Data)
9. Check file paths for eng.ts and raw.ts to make sure they're correct
10. Comment out any sensors with .cfg files that were not installed on the glider
11. If raw NetCDF file includes erroneous GPS hits that affect the map (Figure 1) or the distance traveled calculation, they may need to be filtered out. You may need to render the document to see if this is necessary. If so, comment in any necessary lines (104-105, 108-109) and run lines 106 and 110
12. Line 138: fill in name of glider and deployment location
13. Code chucnk starting on line 201: 
	a. line 210 (`File Name`): change the objects (sensor.file) to the sensors installed on the glider
	b. line 211 (`Sensor`): change the objects (sensor.spec) 
	c. line 212 (`State to Sample`): change "state.to.sample" as appropriate (will usually be c(rep(state.to.sample.15,x)), where x = number of sensors installed
	d. line 214 (`Depth to Sample`): will likely stay the same, but check
	e.lines 215 (`Serial Number`): this will need to be filled in manually
14: Starting on line 221, copy and paste pre-written text detailing the objectives of the deployment
15. The "Pre-Deployment Preparation and Testing" section includes information for Slocum and OceanScout gliders. Delete the non-relevant section
16: Copy and paste pre-written text in the "Deployment" section. Keep line 259 and fill in the glider name ("glider") and deployment vessel. Edit text as necessary for battery configuration and autoballast, but don't change the inline code
17. Line 286: Edit text as necessary but don't change inline code for battery consumption calculations
18. Code chunks starting on line 290 and on line 395 may not be necessary - these chunks create tables of sensor settings throughout a deployment. They are useful if sensor settings were changed. If sensor settings were not changed, these code chunks can be deleted
19. Copy and paste pre-written text into the "Post-Deployment Actions" section
20. Code chunk starting on line 459: ensure file paths and plot names are correct
21. Ensure inline code corresponds to the correct figures in the code chunk above and edit alt text as necessary