# This script expects to be run in the glider-utils Instance in GCP

import os
import logging
import xarray as xr

from esdglider import acoustics, config, gcp, glider, imagery, plots

# Variables for user to update
deployment_info = {
    "deployment": 'amlr08-20220513', 
    "project": "SANDIEGO", 
    "mode": 'delayed', 
    "min_dt": '2022-05-13 18:56:55', 
}
write_nc = True

# Consistent variables
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab/deployment-configs")
file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
deployment_bucket = 'amlr-gliders-deployments-dev'
acoustics_bucket = "amlr-gliders-acoustics-dev"
imagery_raw_bucket = "amlr-gliders-imagery-raw-dev"
deployments_path = os.path.join(base_path, deployment_bucket)
acoustics_path = f"{base_path}/{acoustics_bucket}"
imagery_raw_path = f"{base_path}/{imagery_raw_bucket}"
log_file = os.path.join(
    deployments_path, "logs", 
    f"{deployment_info["deployment"]}-{deployment_info["mode"]}.log"
)
db_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-utils/db/glider-db-prod.txt"
config_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-lab/deployment-configs"

if __name__ == "__main__":
    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(deployment_bucket, deployments_path, ro=False)
    gcp.gcs_mount_bucket(acoustics_bucket, acoustics_path, ro=False)
    gcp.gcs_mount_bucket(imagery_raw_bucket, imagery_raw_path, ro=False)

    logging.basicConfig(
        filename=log_file,
        filemode="w", 
        format='%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')

    # # Create config file - one-time, local run
    # with open(db_path_local, "r") as f:
    #     conn_string = f.read()
    # config.make_deployment_config(
    #     deployment_info = deployment_info, 
    #     config_path_local,
    #     conn_string,
    # )

    paths = glider.get_path_deployment(
        deployment_info = deployment_info, 
        deployments_path=deployments_path,
        config_path=config_path,
    )

    # Generate timeseries and gridded netCDF files
    outname_dict = glider.binary_to_nc(
        deployment_info = deployment_info, 
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info
    )
    tssci = xr.load_dataset(outname_dict["outname_tssci"])
    tseng = xr.load_dataset(outname_dict["outname_tseng"])
    g5sci = xr.load_dataset(outname_dict["outname_5m"])
    
    # Acoustics
    a_paths = acoustics.get_path_acoutics(deployment_info, acoustics_path)
    acoustics.echoview_metadata(tssci, a_paths)

    # Imagery
    i_paths = imagery.get_path_imagery(deployment_info, imagery_raw_path)
    imagery.imagery_timeseries(tssci, i_paths)

    # Plots
    etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    plots.all_loops(
        tssci, tseng, g5sci, crs="Mercator", 
        base_path=paths['plotdir'], bar_file=etopo_path)
        
    # # Generate profile netCDF files for the DAC
    # outname_tssci = os.path.join(paths['tsdir'], f"{deployment}-{mode}-sci.nc")
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'], 
    #     force=True)
