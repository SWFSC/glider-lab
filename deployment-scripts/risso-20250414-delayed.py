import logging
import os

import xarray as xr
from esdglider import acoustics, gcp, glider, plots, utils

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "risso-20250414"
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
        # but this breaks  many other profiles
        tsraw = xr.load_dataset(outname_dict["outname_tsraw"])
        tsraw["profile_index"].loc[
            dict(time=slice("2025-04-15 17:19", "2025-04-15 17:27:17"))
        ] = 88.5

        # Check profiles, and write profile CSV and netcdf
        prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
        prof_summ.to_csv(paths["profsummpath"], index=False)
        utils.check_profiles(prof_summ)        
        utils.to_netcdf_esd(tsraw, outname_dict["outname_tsraw"])

        # Create the rest of the files
        outname_dict = glider.binary_to_nc(
            deployment_info=deployment_info,
            paths=paths,
            write_raw=False,
            write_timeseries=True,
            sci_timeseries_pyglider=False, 
            write_gridded=False,
            file_info=file_info,
            shake=19
        )

        glider.make_gridfiles_depth_measured(paths=paths)


    ### Plots
    etopo_path = os.path.join(base_path, "ETOPO_2022_v1_15s_N45W135_erddap.nc")
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        ds_sci_depth_var="depth_measured", 
        base_path=paths["plotdir"],
        bar_file=etopo_path,
    )
    
    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)

    logging.info("Completed scheduled processing")
