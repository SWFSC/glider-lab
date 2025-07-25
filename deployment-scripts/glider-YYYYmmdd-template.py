import logging
import os

import numpy as np
import xarray as xr
from esdglider import acoustics, gcp, glider, imagery, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = ""
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
    paths = glider.get_path_glider(deployment_info, deployments_path)

    logging.basicConfig(
        filename=os.path.join(paths["logdir"], log_file_name),
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.captureWarnings(True)
    logging.info("Beginning scheduled processing for %s", file_info)

    ### Generate netCDF files and plots
    # outname_dict = glider.binary_to_nc(
    #     deployment_info=deployment_info,
    #     paths=paths,
    #     write_raw=write_nc,
    #     write_timeseries=write_nc,
    #     write_gridded=write_nc,
    #     file_info=file_info,
    # )

    ### Make any adjustments to netCDF files
    # if write_nc:
    #     logging.info("Adjusting datasets, after review")
    #     tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
    #     tseng = xr.load_dataset(outname_dict["outname_tseng"])
    #     tssci = xr.load_dataset(outname_dict["outname_tssci"])

    ### Sensor-specific processing
    # tssci = xr.load_dataset(outname_dict["outname_tssci"])
    # tseng = xr.load_dataset(outname_dict["outname_tseng"])
    # g5sci = xr.load_dataset(outname_dict["outname_5m"])

    # # Acoustics
    # a_paths = acoustics.get_path_acoustics(deployment_info, acoustics_path)
    # acoustics.echoview_metadata(tssci, a_paths)

    # # Imagery
    # i_paths = imagery.get_path_imagery(deployment_info, imagery_path)
    # imagery.imagery_timeseries(tssci, i_paths)

    ### Plots
    # etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    # plots.esd_all_plots(
    #     outname_dict,
    #     crs="Mercator",
    #     base_path=paths["plotdir"],
    #     bar_file=etopo_path,
    # )
    # ## OR, for Antarctic ##
    # plots.esd_all_plots(outname_dict, crs=None, base_path=paths["plotdir"])
    # plots.sci_surface_map_loop(
    #     xr.load_dataset(outname_dict["outname_gr5m"]),
    #     crs="Mercator",
    #     base_path=paths["plotdir"],
    #     figsize_x=11,
    #     figsize_y=8.5,
    # )

    ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
