import logging

# import numpy as np
# import xarray as xr
from pathlib import Path

from esdglider.slocum import pipeline

from esdglider import gcp, paths, plots, qartod

logger = logging.getLogger(__name__)

### Variables for user to update
deployment_name = "risso-20260128"
mode = "delayed"
write_nc = True
sci_use_m_depth = True

### Consistent variables
# Define directories
home = Path.home()
mnt_path = home / "gcs-mnt"
mnt_path = home / "mnt-gcs"
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

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).name}"
log_file_name = f"{deployment_name}-{mode}.log"

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

    # Generate glider paths
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
    # ### Timeseries and gridded netCDF generation
    # Generate timeseries and gridded netCDF files
    outname_dict_ts = pipeline.generate_timeseries(
        deployment_name = deployment_name, 
        mode = mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_eng=write_nc,
        write_sci=write_nc,
        sci_use_m_depth=sci_use_m_depth, 
        file_info=file_info,
        binary_search="*.[DEde][Cc][Dd]"
    )

    # # Correct profiles, and make other adjustments to netCDF files, if necessary
    # if write_nc:
    #     logger.info("Adjusting datasets, after review---------------------")
    #     tsraw = xr.load_dataset(outname_dict_ts["outname_tsraw"])
    #     tseng = xr.load_dataset(outname_dict_ts["outname_tseng"])
    #     tssci = xr.load_dataset(outname_dict_ts["outname_tssci"])

    #     # Adjust profile index
    #     logger.info("Correcting profile_index for raw, eng, and sci datasets")
    #     # tssci["profile_index"].loc[{"time": "2024-11-13 15:14:59"}] = 590.5
    #     tsraw["profile_index"].loc[
    #         {"time": slice("2026-02-01 09:05", "2026-02-01 09:16:10")}
    #     ] = 397

    #     pipeline.complete_profile_correction(
    #         tsraw,
    #         tseng,
    #         tssci,
    #         glider_paths=glider_paths,
    #     )

    # Create qc variables for science netCDF files, after corrections
    if write_nc:
        logger.info("Generating qc flags---------------------")
        qartod.run_qartod_qc(
            input_file=outname_dict_ts["outname_tssci"],
            output_file=outname_dict_ts["outname_tssci"],
            overwrite_qc=True
        )

    # logger.info("Generating gridded netCDF files---------------------")
    # outname_dict_gr = pipeline.generate_gridded(
    #     glider_paths=glider_paths,
    #     write_gridded=write_nc,
    # )

    # outname_dict = outname_dict_ts | outname_dict_gr


    #--------------------------------------------------------------------------
    # ### Ancillary data products
    

    # ## Plots
    # plots.esd_all_plots(
    #     outname_dict,
    #     crs="Mercator",
    #     base_path=glider_paths["plotdir"],
    # )

    ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     glider_paths['profdir'], 
    #     glider_paths['deploymentyaml'],
    #     force=True, 
    # )

    #--------------------------------------------------------------------------
    logger.info("Completed scheduled processing")
