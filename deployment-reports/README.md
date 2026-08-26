README for glider report template

1.  Make a copy of REPORT_TEMPLATE in "\~/glider-lab/deployment-reports"
2.  Rename REPORT_TEMPLATE.qmd with the glider deployment name (e.g., risso-20250414)
3.  Choose processor and access deployment data
    a.  If working on local machine, download data from GCP and save to "\~/glider-lab/deployment-reports/Data/glider-yyyymmdd/", including;
        i.  all .ma files from swfscesd-glider-deployments-data-in/year/glider-yyyymmdd/archive-sfmc
        ii. raw netCDF (glider-yyyymmdd-delayed-raw.nc) from swfscesd-glider-deployments-data-out/year/glider-yyyymmdd/processed-L0
        iii. science and engineering netCDFs (glider-yyyymmdd-delayed-eng.nc & glider-yyyymmdd-delayed-sci.nc) from swfscesd-glider-deployments-data-out/year/glider-yyyymmdd/processed-L1
        iv. output spatial grid plots from swfscesd-glider-deployments-data-out/year/glider-yyyymmdd/plots/delayed/spatialGrids-sci
    b.  If working on cloud workstation, ensure your buckets are mounted... TODO
4.  In the .qmd document, fill in glider name and deployment date on line 2
5.  In first code chunk;
    a.  Update lines 38-47 with deployment specific metadata
    b.  Update lines 49-68, commenting in which sensors this glider was deployed with
    c.  Update lines 70-78 with sensor serial numbers
    d.  Update line 86 to "Local" or "GCP" depending on where you are running this script
6.  If raw NetCDF file includes erroneous GPS hits that affect the map (Figure 1) or the distance traveled calculation, they may need to be filtered out. You may need to render the document to see if this is necessary. If so, comment in any necessary lines (108-109, 112-113) and run lines 110 and 114
7.  Starting on line 235, copy and paste pre-written text detailing the objectives of the deployment
8.  The "Pre-Deployment Preparation and Testing" section includes information for Slocum and OceanScout gliders. Delete the non-relevant section
9.  Copy and paste pre-written text in the "Deployment" section. Keep line 273 and fill in the glider name ("glider") and deployment vessel. Edit text as necessary for battery configuration and autoballast, but don't change the inline code
10. Line 301: Edit text as necessary but don't change inline code for battery consumption calculations
11. Code chunks starting on line 305 and on line 411 may not be necessary - these chunks create tables of sensor settings throughout a deployment. They are useful if sensor settings were changed. If sensor settings were not changed, these code chunks can be deleted
12. Copy and paste pre-written text into the "Post-Deployment Actions" section
13. Code chunk starting on line 475: ensure file paths and plot names are correct
14. Ensure inline code corresponds to the correct figures in the code chunk above and edit alt text as necessary