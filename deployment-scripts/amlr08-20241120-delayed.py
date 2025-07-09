# This script expects to be run in the glider-utils Instance in GCP

import logging
import os

import numpy as np
import xarray as xr
from esdglider import acoustics, gcp, glider, imagery, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "amlr08-20241120"
mode = "delayed"
write_nc = True

# Other variables used throughout the script
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
deployments_bucket = "amlr-gliders-deployments-dev"
deployments_path = os.path.join(base_path, deployments_bucket)
acoustics_bucket = "amlr-gliders-acoustics-dev"
acoustics_path = f"{base_path}/{acoustics_bucket}"
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
    gcp.gcs_mount_bucket(acoustics_bucket, acoustics_path, ro=False)
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

    ### Decompress binary files
    glider.decompress(paths["binarydir"])

    ### Generate netCDF files and plots
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info,
    )

    ### Because the glider errored, need to handle the last profile
    if write_nc:
        logging.info("Adjusting datasets, after review")
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict["outname_tseng"])
        tssci = xr.load_dataset(outname_dict["outname_tssci"])

        # Adjust profile index
        logging.info("Removing bogus time values from after glider was recovered")
        max_time = np.datetime64("2024-11-25")
        logging.info("Num of points dropped for raw, eng, and sci:")
        for i in [tsraw, tseng, tssci]:
            logging.info(np.count_nonzero(i.time > max_time))
        
        tsraw = tsraw.sel(time=tsraw.time < max_time)
        tseng = tseng.sel(time=tseng.time < max_time)

        logging.info("Correcting profile_index for raw and eng datasets")
        time_slice = slice("2024-11-24 11:00", "2024-11-25")
        prof_last = np.max(tsraw.profile_index.values)
        tsraw["profile_index"].loc[dict(time=time_slice)] = prof_last
        tseng["profile_index"].loc[dict(time=time_slice)] = prof_last
        prof_summ = utils.calc_profile_summary(tsraw)
        prof_summ.to_csv(paths["profsummpath"], index=False)

        # Profile checks
        utils.check_profiles(tsraw)
        utils.check_profiles(tseng)
        utils.check_profiles(tssci)

        # Write to Netcdf, and rerun gridding
        logging.info("Write timeseries to netcdf")
        utils.to_netcdf_esd(tsraw, outname_dict["outname_tsraw"])
        utils.to_netcdf_esd(tseng, outname_dict["outname_tseng"])
        del tsraw, tssci, tseng

        logging.info(
            "Regenerating gridded data not necessary, "
            + "because no changes to sci timeseries"
        )

    ### Plots
    plots.esd_all_plots(outname_dict, crs=None, base_path=paths["plotdir"])
    plots.sci_surface_map_loop(
        xr.load_dataset(outname_dict["outname_gr5m"]),
        crs="Mercator",
        base_path=paths["plotdir"],
        figsize_x=11,
        figsize_y=8.5,
    )

    ### Sensor-specific processing
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

    # Acoustics
    a_paths = acoustics.get_path_acoutics(deployment_info, acoustics_path)
    acoustics.echoview_metadata(tssci, a_paths)

    # ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
