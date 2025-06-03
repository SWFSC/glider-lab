# This script expects to be run in the glider-utils Instance in GCP

import logging
import os

import xarray as xr
from esdglider import acoustics, gcp, glider, plots, utils

# # Variables for user to update
# deployment_info = {
#     "deployment": "unit_1024-20250224",
#     "project": "SANDIEGO",
#     "mode": "delayed",
#     "min_dt": "2025-02-24",
# }
# write_nc = True

# # Consistent variables
# base_path = "/home/sam_woodman_noaa_gov"
# config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
# deployment_bucket = "amlr-gliders-deployments-dev"
# deployments_path = os.path.join(base_path, deployment_bucket)
# # acoustics_bucket = "amlr-gliders-acoustics-dev"
# # acoustics_path = f"{base_path}/{acoustics_bucket}"
# # imagery_bucket = "amlr-gliders-imagery-raw-dev"
# # imagery_path = f"{base_path}/{imagery_bucket}"

# file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
# log_file_name = f"{deployment_info['deployment']}-{deployment_info['mode']}.log"
# log_file = os.path.join(deployments_path, "logs", log_file_name)
# db_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-utils/db/glider-db-prod.txt"
# config_path_local = "C:/SMW/Gliders_Moorings/Gliders/glider-lab/deployment-configs"

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "unit_1024-20250224"
mode = "delayed"
write_nc = True

# Other variables used throughout the script
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
deployments_bucket = "amlr-gliders-deployments-dev"
deployments_path = os.path.join(base_path, deployments_bucket)
# acoustics_bucket = "amlr-gliders-acoustics-dev"
# acoustics_path = f"{base_path}/{acoustics_bucket}"
# imagery_bucket = "amlr-gliders-imagery-raw-dev"
# imagery_path = f"{base_path}/{imagery_bucket}"

deployment_info = {
    "deploymentyaml": os.path.join(config_path, f"{deployment_name}.yml"), 
    "mode": mode,
}
file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
log_file_name = f"{deployment_name}-{mode}.log"

if __name__ == "__main__":
    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(deployments_bucket, deployments_path, ro=False)
    # gcp.gcs_mount_bucket(acoustics_bucket, acoustics_path, ro=False)
    # gcp.gcs_mount_bucket(imagery_bucket, imagery_path, ro=False)
    paths = glider.get_path_deployment(deployment_info, deployments_path)

    logging.basicConfig(
        filename=os.path.join(paths["logdir"], log_file_name),
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Beginning scheduled processing for %s", file_info)

    ## Generate netCDF files and plots
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info,
        stall=10,
        interrupt=600,
    )

    # Plots
    plots.esd_all_plots(outname_dict, crs="Mercator", base_path=paths["plotdir"])

    ### Sensor-specific processing
    # tssci = xr.load_dataset(outname_dict["outname_tssci"])
    # tseng = xr.load_dataset(outname_dict["outname_tseng"])
    # g5sci = xr.load_dataset(outname_dict["outname_5m"])

    # Acoustics
    # a_paths = acoustics.get_path_acoutics(deployment_info, acoustics_path)
    # acoustics.echoview_metadata(tssci, a_paths)

    # Imagery
    # i_paths = imagery.get_path_imagery(deployment_info, imagery_raw_path)
    # imagery.imagery_timeseries(tssci, i_paths)

    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)
