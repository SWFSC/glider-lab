import logging
from pathlib import Path

# import numpy as np
import xarray as xr
from esdglider import gcp, paths, plots, slocum, utils # type: ignore


# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "risso-20250414"
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
# imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
# imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
# aa_path = mnt_path / aa_bucket_name
# imagery_in_path = mnt_path / imagery_in_bucket_name
# imagery_meta_path = mnt_path / imagery_meta_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).stem}"
log_file_name = f"{Path(__file__).stem}.log"


if __name__ == "__main__":
    gcp.gcs_mount_bucket(logs_bucket_name, logs_path, ro=False)
    gcp.gcs_mount_bucket(data_in_bucket_name, data_in_path, ro=True)
    gcp.gcs_mount_bucket(data_out_bucket_name, data_out_path, ro=False)

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

    ## Generate netCDF files and plots
    outname_dict = slocum.binary_to_nc(
        deployment_name=deployment_name, 
        mode=mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_timeseries=False,
        write_gridded=False,
        file_info=file_info,
        shake=19
    )

    """
    NOTE
    The raw dataset has several (n=23) instances of the CTD being off, 
    turning back on, and thus recording one bogus point while it still 
    has its pressure from the last time the CTD was on.
    However, all of these are in 0.5 profiles, 
    and so will not be propogated to the published data

    Additionally, because the CTD was turned off during this deployment, 
    we need to grid using depth_measured
    """

    if write_nc:
        logging.info("Adjusting datasets, after review")
        # Risso had one surface profile that dipped to 5m, which triggered a 
        # new profile. The fix for this would be to change stall to 5, 
        # but this breaks many other profiles
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tsraw["profile_index"].loc[
            dict(time=slice("2025-04-15 17:19", "2025-04-15 17:27:17"))
        ] = 88.5

        # Check profiles, and write profile CSV and netcdf
        prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
        prof_summ.to_csv(glider_paths["profsummpath"], index=False)
        utils.check_profiles(prof_summ)        
        utils.to_netcdf_esd(tsraw, outname_dict["outname_tsraw"])

        # Create the rest of the files
        outname_dict = slocum.binary_to_nc(
            deployment_name=deployment_name, 
            mode=mode, 
            glider_paths=glider_paths,
            write_raw=False,
            write_timeseries=True,
            sci_timeseries_pyglider=False, 
            write_gridded=False,
            file_info=file_info,
            shake=19
        )

        slocum.make_gridfiles_depth_measured(glider_paths=glider_paths)


    ### Plots
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        ds_sci_depth_var="depth_measured", 
        base_path=glider_paths["plotdir"],
        bar_file=etopo_path,
    )
    
    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)

    logging.info("Completed scheduled processing")
