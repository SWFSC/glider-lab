import logging
import os

import numpy as np
import xarray as xr
from esdglider import acoustics, gcp, glider, imagery, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "amlr01-20241120"
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
        filemode="a",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Beginning scheduled processing for %s", file_info)

    logging.info("No decompressing needed - software v8.6")

    profargs = {
        "stall": 15,
        # "shake": 20, 
        # "interrupt": 180,
        # "inversion": 3, 
        # "length": 10, 
        # "period": 0, 
    }

    ### Generate netCDF files and plots
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=write_nc,
        file_info=file_info,
        **profargs, 
        # stall=15,
        # shake=20, 
        # interrupt=180,
        # inversion=3, 
        # length=5, 
        # period=0, 
    )

    if write_nc:
        logging.info("Adjusting datasets after review")
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict["outname_tseng"])
        tssci = xr.load_dataset(outname_dict["outname_tssci"])

        logging.info("Correcting profile_index for raw, eng, and sci datasets")
        # Remove a particular timestamp, and rerun profile calculations
        # This timestamp was breaking profile calculations, and parameters
        # could not be tuned to handle both this timestamp and rest of data
        # We run eng and sci timeseries through this function as well for simplicity
        time_toremove = "2024-12-13 03:24:07.488281344"
        tsraw = glider.drop_ts_ranges(
            tsraw, 
            drop_list=[(time_toremove, time_toremove)], 
            ds_type="raw", 
            profsummdir=paths["profsummpath"], 
            outname=outname_dict["outname_tsraw"], 
            **profargs, 
        )
        logging.info("eng")
        tseng = glider.drop_ts_ranges(
            tseng, 
            drop_list=[(time_toremove, time_toremove)], 
            ds_type="eng", 
            profsummdir=paths["profsummpath"], 
            outname=outname_dict["outname_tseng"], 
        )
        logging.info("sci")
        tssci = glider.drop_ts_ranges(
            tssci, 
            drop_list = [(time_toremove, time_toremove)], 
            ds_type="sci", 
            profsummdir=paths["profsummpath"], 
            outname=outname_dict["outname_tssci"], 
        )

        # time_toremove = np.datetime64("2024-12-13 03:24:07.488281344")
        # logging.info(
        #     "Dropping %s points from the raw dataset, for profile calcs", 
        #     np.count_nonzero(tsraw.time.values == time_toremove)
        # )

        # # Calculate new profiles for raw dataset
        # tsraw = tsraw.sel(time=(tsraw.time != time_toremove))
        # tsraw = utils.get_fill_profiles(tsraw, tsraw.time.values, tsraw.depth.values, **kwargs)
        # prof_summ = utils.calc_profile_summary(tsraw)
        # prof_summ.to_csv(paths["profsummpath"], index=False)

        # 'Calculate', ie join, profiles for eng and sci timeseries
        # tseng = utils.join_profiles(tseng, prof_summ, **kwargs)
        # tssci = utils.join_profiles(tssci, prof_summ, **kwargs)

        # # Profile checks
        # utils.check_profiles(tsraw)
        # utils.check_profiles(tseng)
        # utils.check_profiles(tssci)

        # # Write to Netcdf, and rerun gridding
        # logging.info("Write timeseries to netcdf")
        # utils.to_netcdf_esd(tsraw, outname_dict["outname_tsraw"])
        # utils.to_netcdf_esd(tseng, outname_dict["outname_tseng"])
        # utils.to_netcdf_esd(tssci, outname_dict["outname_tssci"])
        del tsraw, tssci, tseng

        logging.info("Regenerating gridded data")
        outname_dict = glider.binary_to_nc(
            deployment_info=deployment_info,
            paths=paths,
            write_raw=False,
            write_timeseries=False,
            write_gridded=True,
            file_info=file_info,
        )        

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
    # tseng = xr.load_dataset(outname_dict["outname_tseng"])
    # g5sci = xr.load_dataset(outname_dict["outname_5m"])

    # Acoustics
    a_paths = acoustics.get_path_acoutics(deployment_info, acoustics_path)
    acoustics.echoview_metadata(tssci, a_paths)

    # Imagery
    # i_paths = imagery.get_path_imagery(deployment_info, imagery_raw_path)
    # imagery.imagery_timeseries(tssci, i_paths)

    # ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     paths['profdir'], 
    #     paths['deploymentyaml'],
    #     force=True, 
    # )

    logging.info("Completed scheduled processing")
