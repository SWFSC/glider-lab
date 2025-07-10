# This script expects to be run in the glider-utils Instance in GCP

import logging
import os

import xarray as xr
from esdglider import acoustics, gcp, glider, plots, utils, imagery

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "george-20240530"
mode = "delayed"
write_nc = True

# Other variables used throughout the script
base_path = "/home/sam_woodman_noaa_gov"
config_path = os.path.join(base_path, "glider-lab", "deployment-configs")
deployments_bucket = "amlr-gliders-deployments-dev"
deployments_path = os.path.join(base_path, deployments_bucket)
# acoustics_bucket = "amlr-gliders-acoustics-dev"
# acoustics_path = f"{base_path}/{acoustics_bucket}"
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
    gcp.gcs_mount_bucket(imagery_bucket, imagery_path, ro=False)
    paths = glider.get_path_deployment(deployment_info, deployments_path)

    logging.basicConfig(
        filename=os.path.join(paths["logdir"], log_file_name),
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Beginning scheduled processing for %s", file_info)

    ### Generate netCDF files and plots
    outname_dict = glider.binary_to_nc(
        deployment_info=deployment_info,
        paths=paths,
        write_raw=write_nc,
        write_timeseries=write_nc,
        write_gridded=False,
        file_info=file_info,
        stall=0, 
        interrupt=600,
    )

    ## Make any adjustments to netCDF files
    if write_nc:
        logging.info("Adjusting profiles in the datasets, after review")
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict["outname_tseng"])
        tssci = xr.load_dataset(outname_dict["outname_tssci"])

        # Because of george's diving patterns, we need to use stall=0 to
        # calculate the correct dives/climbs using stall=0. However, 
        # this leaves several profiles that need adjusting around the edges
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-16 14:08", "2024-06-16 14:18:58.02"))
        ] = 262
        tsraw["profile_index"].loc[
            dict(time=slice("2024-05-30 19:06", "2024-05-30 19:10:52.03"))
        ] = 4.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-05-30 23:46", "2024-05-30 23:53:22"))
        ] = 16.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-08 01:17", "2024-06-08 01:24:42"))
        ] = 148.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-10 14:44:44", "2024-06-10 14:48"))
        ] = 180.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-11 22:09", "2024-06-11 22:22:34.2"))
        ] = 204.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-13 17:09", "2024-06-13 17:20:48.12"))
        ] = 228.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-15 01:39", "2024-06-15 02:00:30"))
        ] = 244.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-15 21:47", "2024-06-15 22:05:26"))
        ] = 252.5
        tsraw["profile_index"].loc[
            dict(time=slice("2024-06-16 08:30", "2024-06-16 08:46"))
        ] = 256.5

        # Expected warning: "There are 1 profiles with more than 180s at 
        # depths less than or equal to 5m. Profile indices: 262.0
        prof_summ = utils.check_profiles(tsraw)        
        prof_summ = utils.calc_profile_summary(tsraw)
        prof_summ.to_csv(paths["profsummpath"], index=False)

        # Apply profiles to eng and sci datasets
        tseng = utils.join_profiles(tseng, utils.calc_profile_summary(tsraw))
        utils.check_profiles(tseng)        
        tssci = utils.join_profiles(tssci, utils.calc_profile_summary(tsraw))
        utils.check_profiles(tssci)

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

    ### Plots
    etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=paths["plotdir"],
        bar_file=etopo_path,
    )

    ### Sensor-specific processing
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

    # Imagery
    i_paths = imagery.get_path_imagery(deployment_info, imagery_path)
    imagery.imagery_timeseries(tssci, i_paths)

    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)
