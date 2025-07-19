# This script expects to be run in the glider-utils Instance in GCP

import logging
import os

import xarray as xr
from esdglider import acoustics, gcp, glider, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "stenella-20250414"
mode = "delayed"
write_nc = True

# Other variables used throughout the script
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
deployments_bucket = "amlr-gliders-deployments-dev"
deployments_path = os.path.join(base_path, deployments_bucket)

deployment_info = {
    "deploymentyaml": os.path.join(config_path, f"{deployment_name}.yml"), 
    "mode": mode,
}
file_info = f"https://github.com/SWFSC/glider-lab: {os.path.basename(__file__)}"
log_file_name = f"{deployment_name}-{mode}.log"

if __name__ == "__main__":
    # Mount the deployments bucket, and generate paths dictionary
    gcp.gcs_mount_bucket(deployments_bucket, deployments_path, ro=False)
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
        write_timeseries=True,
        sci_timeseries_pyglider=False, 
        write_gridded=True,
        file_info=file_info,
        shake=10,
    )

    """
    NOTE
    The stenella raw dataset has several (~20) instances of the CTD being off, 
    turning back on, and thus recording one bogus point while it still 
    has its pressure from the last time the CTD was on.
    
    However, we do not need to fix, as all of these are in 0.5 profiles, 
    and thus none are propagated through to the science timeseries
    """

    ## Plots
    etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=paths["plotdir"],
        bar_file=etopo_path,
    )

    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)
