import logging
from pathlib import Path

from esdglider.slocum import pipeline

from esdglider import gcp, paths, plots, qartod

logger = logging.getLogger(__name__)

# Variables for user to update. All other deployment info is in the yaml file
deployment_name = "stenella-20250414"
mode = "delayed"
write_nc = True
sci_use_m_depth = True
profile_args = {
    "shake": 10,
}
### Consistent variables
# Define directories
home = Path.home()
mnt_path = home / "mnt-gcs"
cac_path = home / "standard-glider-files" / "Cache"
config_path = home / "glider-lab" / "deployment-configs"

# Bucket names and paths
logs_bucket_name = "swfscesd-glider-logs"
data_in_bucket_name = "swfscesd-glider-deployments-data-in"
data_out_bucket_name = "swfscesd-glider-deployments-data-out"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).stem}"
log_file_name = f"{Path(__file__).stem}.log"

#------------------------------------------------------------------------------
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
    logger.info("Beginning scheduled processing for %s", file_info)
    print(f"Writing logs to {logs_path / log_file_name}")

    logger.info("Generating glider paths")
    glider_paths = paths.get_path_glider(
        deployment_name = deployment_name, 
        mode = mode, 
        config_path = config_path, 
        data_in_path = data_in_path, 
        data_out_path = data_out_path, 
        cac_path = cac_path, 
    )

    #--------------------------------------------------------------------------
    ### Timeseries and gridded netCDF generation
    outname_dict_ts = pipeline.generate_timeseries(
        deployment_name=deployment_name, 
        mode=mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_eng=write_nc,
        write_sci=write_nc,
        sci_use_m_depth=sci_use_m_depth, 
        file_info=file_info,
        prof_args=profile_args, 
    )

    """
    NOTE    
    The raw dataset has several (n=21) instances of the CTD being off,
    turning back on, and thus recording one bogus point while it still 
    has its pressure from the last time the CTD was on.
    However, all of these are in 0.5 profiles, 
    and so will not be propagated to the published data
    """

    if write_nc:
        # Create qc variables for science netCDF files, after corrections
        logger.info("Generating qc flags---------------------")
        qartod.run_qartod_qc(
            input_file=outname_dict_ts["outname_tssci"],
            output_file=outname_dict_ts["outname_tssci"],
            overwrite_qc=True
        )

    #--------------------------------------------------------------------------
    ### Write gridded data
    logger.info("Generating gridded netCDF files---------------------")
    outname_dict_gr = pipeline.generate_gridded(
        glider_paths=glider_paths,
        write_gridded=write_nc,
    )

    outname_dict = outname_dict_ts | outname_dict_gr

    #--------------------------------------------------------------------------
    ### Plots
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        bar_file=str(etopo_path),
    )

    #--------------------------------------------------------------------------
    ### Generate profile netCDF files for the DAC
    # process.ngdac_profiles(
    #     outname_tssci, paths['profdir'], paths['deploymentyaml'],
    #     force=True)

    #--------------------------------------------------------------------------
    logger.info("Completed scheduled processing")
