# This script expects to be run in the glider-utils Instance in GCP

import os
import logging
import xarray as xr

from esdglider import acoustics, config, gcp, glider, plots

# Variables for user to update
deployment = 'calanus-20241019'
project = "ECOSWIM"
mode = 'delayed'
min_dt='2024-10-19 17:37:00'
write_nc = False

# Consistent variables
base_path = "/home/sam_woodman_noaa_gov"
file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
deployment_bucket = 'amlr-gliders-deployments-dev'
acoustics_bucket = "amlr-gliders-acoustics-dev"

config_path = os.path.join(base_path, "glider-lab/deployment-configs")
deployments_path = os.path.join(base_path, deployment_bucket)
acoustics_path = f"{base_path}/{acoustics_bucket}"

db_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-utils/db/glider-db-prod.txt"
config_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-lab/deployment-configs"

if __name__ == "__main__":
    logging.basicConfig(
        format='%(module)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')

    # # Create config file - one-time, local run
    # with open(db_path_local, "r") as f:
    #     conn_string = f.read()
    # config.make_deployment_config(
    #     deployment,
    #     project,
    #     config_path_local,
    #     conn_string,
    # )

    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(deployment_bucket, deployments_path, ro=False)
    gcp.gcs_mount_bucket(acoustics_bucket, acoustics_path, ro=False)

    paths = glider.get_path_deployment(
        project=project,
        deployment=deployment,
        mode=mode,
        deployments_path=deployments_path,
        config_path=config_path,
    )

    # Generate timeseries and gridded netCDF files
    outname_tseng, outname_tssci, outname_1m, outname_5m = glider.binary_to_nc(
        deployment=deployment,
        mode=mode,
        paths=paths,
        min_dt=min_dt,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info, 
    )
    tssci = xr.load_dataset(outname_tssci)
    tseng = xr.load_dataset(outname_tseng)
    g5sci = xr.load_dataset(outname_5m)

    # # Acoustics
    # a_paths = acoustics.get_path_acoutics(project, deployment, acoustics_path)
    # acoustics.echoview_metadata(tssci, a_paths)

    # Plots
    etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    plots.all_loops(tssci, tseng, g5sci, paths['plotdir'], etopo_path)
        
    # # Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'], 
    #     force=True)
