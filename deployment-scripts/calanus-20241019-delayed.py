# This script expects to be run in the glider-utils Instance in GCP

import logging
import os

import numpy as np
import xarray as xr
from esdglider import acoustics, gcp, glider, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "calanus-20241019"
mode = "delayed"
write_nc = True

# Consistent variables
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
deployments_bucket = "amlr-gliders-deployments-dev"
deployments_path = os.path.join(base_path, deployments_bucket)
acoustics_bucket = "amlr-gliders-acoustics-dev"
acoustics_path = f"{base_path}/{acoustics_bucket}"
imagery_bucket = "amlr-gliders-imagery-raw-dev"
imagery_path = f"{base_path}/{imagery_bucket}"

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
    paths = glider.get_path_deployment(deployment_info, deployments_path)

    logging.basicConfig(
        filename=os.path.join(paths["logdir"], log_file_name),
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Beginning scheduled processing for %s", file_info)

    # Generate timeseries and gridded netCDF files
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info,
        stall=2,
        interrupt=120,
    )

    # --------------------------------------------------------------------------
    # Science dataset trimming
    if write_nc:
        logging.info("Adjusting datasets after review")
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict["outname_tseng"])
        tssci = xr.load_dataset(outname_dict["outname_tssci"])

        # Adjust profile index
        logging.info("Correcting profile_index for raw, eng, and sci datasets")
        # tssci["profile_index"].loc[dict(time="2024-11-13 15:14:59")] = 590.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-11-01 18:18", "2024-11-01 18:19"))
        ] = 356.5
        tseng["profile_index"].loc[
            dict(time=slice("2024-11-01 18:18", "2024-11-01 18:19"))
        ] = 356.5
        tssci["profile_index"].loc[
            dict(time=slice("2024-11-01 18:18", "2024-11-01 18:19"))
        ] = 356.5

        # Drop a specific sci value - confirmed ok in eng
        tssci = tssci.where(
            (tssci["time"] != np.datetime64("2024-11-01 18:58:36.312000")),
            drop=True,
        )

        # Drop time ranges with bogus lat/lons
        logging.info(
            "Dropping time ranges with bogus lat/lons from eng and sci datasets",
        )
        drop_ranges = [
            ("2024-10-21 14:26:50", "2024-10-21 19:52:30"),
            ("2024-11-09 13:15", "2024-11-09 18:10"),
            ("2024-11-14 01:00", "2024-11-14 01:10:20"),
        ]
        tseng = glider.drop_ts_ranges(tseng, drop_ranges, "eng", paths["plotdir"])
        tssci = glider.drop_ts_ranges(tssci, drop_ranges, "sci", paths["plotdir"])

        # Write profile summary        
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
        utils.to_netcdf_esd(tssci, outname_dict["outname_tssci"])
        del tsraw, tssci, tseng

        logging.info("ReGenerating gridded data")
        outname_dict = glider.binary_to_nc(
            deployment_info=deployment_info,
            paths=paths,
            write_raw=False,
            write_timeseries=False,
            write_gridded=True,
            file_info=file_info,
        )
    # --------------------------------------------------------------------------

    # Acoustics
    tssci = xr.load_dataset(outname_dict["outname_tssci"])
    a_paths = acoustics.get_path_acoutics(deployment_info, acoustics_path)
    acoustics.echoview_metadata(tssci, a_paths)

    # Plots
    etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=paths["plotdir"],
        bar_file=etopo_path,
    )

    # Generate profile netCDF files for the DAC
    glider.ngdac_profiles(
        outname_dict["outname_tssci"], 
        paths['profdir'], 
        paths['deploymentyaml'],
        force=True, 
    )

    logging.info("Completed scheduled processing")
