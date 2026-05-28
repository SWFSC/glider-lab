import logging
from pathlib import Path
import xarray as xr
from esdglider import gcp, paths, plots, slocum, utils, imagery

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "george-20240530"
mode = "delayed"
write_nc = True

### Consistent variables
# Define directories
home = Path.home()
mnt_path = home / "gcs-mnt"
cac_path = home / "standard-glider-files" / "Cache"
config_path = home / "glider-lab" / "deployment-configs"

# Bucket names and paths
logs_bucket_name = "swfscesd-glider-logs"
data_in_bucket_name = "swfscesd-glider-deployments-data-in"
data_out_bucket_name = "swfscesd-glider-deployments-data-out"
# aa_bucket_name = "swfscesd-glider-active-acoustics-data-in"
imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
# aa_path = mnt_path / aa_bucket_name
imagery_in_path = mnt_path / imagery_in_bucket_name
imagery_meta_path = mnt_path / imagery_meta_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).name}"
log_file_name = f"{deployment_name}-{mode}.log"

if __name__ == "__main__":
    gcp.gcs_mount_bucket(logs_bucket_name, logs_path, ro=False)
    gcp.gcs_mount_bucket(data_in_bucket_name, data_in_path, ro=True)
    gcp.gcs_mount_bucket(data_out_bucket_name, data_out_path, ro=False)
    gcp.gcs_mount_bucket(imagery_in_bucket_name, imagery_in_path, ro=True)
    gcp.gcs_mount_bucket(imagery_meta_bucket_name, imagery_meta_path, ro=True)

    logging.basicConfig(
        filename=logs_path / log_file_name,
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.captureWarnings(True)
    logging.info("Beginning scheduled processing for %s", file_info)

    # Generate glider paths
    glider_paths = paths.get_path_glider(
        deployment_name = deployment_name, 
        mode = mode, 
        config_path = config_path, 
        data_in_path = data_in_path, 
        data_out_path = data_out_path, 
        cac_path = cac_path, 
    )

    ### Generate netCDF files and plots
    outname_dict = slocum.binary_to_nc(
        deployment_name=deployment_name, 
        mode=mode, 
        glider_paths=glider_paths,
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
        # depths less than or equal to 5m. Profile indices: 262.0"
        prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
        prof_summ.to_csv(glider_paths["profsummpath"], index=False)
        utils.check_profiles(prof_summ)        

        # Apply profiles to eng and sci datasets
        tseng = utils.join_profiles(tseng, prof_summ)
        utils.check_profiles(utils.calc_profile_summary(tseng, "depth"))
        tssci = utils.join_profiles(tssci, prof_summ)
        utils.check_profiles(utils.calc_profile_summary(tssci, "depth"))

        logging.info("Write timeseries to netcdf")
        utils.to_netcdf_esd(tsraw, outname_dict["outname_tsraw"])
        utils.to_netcdf_esd(tseng, outname_dict["outname_tseng"])
        utils.to_netcdf_esd(tssci, outname_dict["outname_tssci"])
        del tsraw, tssci, tseng

        logging.info("Generating gridded data, after profile adjustment")
        outname_dict = slocum.binary_to_nc(
            deployment_name=deployment_name, 
            mode=mode, 
            glider_paths=glider_paths,
            write_raw=False,
            write_timeseries=False,
            write_gridded=True,
            file_info=file_info,
        )

    ### Sensor-specific processing
    tssci = xr.load_dataset(outname_dict["outname_tssci"])

    # Imagery
    img_paths = paths.get_path_imagery(
        deployment_name = deployment_name, 
        imagery_in_path = imagery_in_path, 
        imagery_meta_path = imagery_meta_path, 
        data_out_path = data_out_path, 
    )
    imagery.imagery_timeseries(tssci, img_paths)

    ### Plots
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        bar_file=etopo_path,
    )

    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)

    logging.info("Completed scheduled processing")
