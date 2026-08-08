import logging
from pathlib import Path

# import numpy as np
import xarray as xr
from esdglider import gcp, imagery, paths, plots, utils # type: ignore
from esdglider.slocum import pipeline # type: ignore

logger = logging.getLogger(__name__)

### Variables for user to update
deployment_name = "calanus-20260403"
mode = "delayed"
write_nc = True

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
## aa_in_bucket_name = "swfscesd-glider-active-acoustics-data-in"
imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = mnt_path / logs_bucket_name
data_in_path = mnt_path / data_in_bucket_name
data_out_path = mnt_path / data_out_bucket_name
# aa_in_path = mnt_path / aa_in_bucket_name
imagery_in_path = mnt_path / imagery_in_bucket_name
imagery_meta_path = mnt_path / imagery_meta_bucket_name

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).stem}"
log_file_name = f"{Path(__file__).stem}.log"


#------------------------------------------------------------------------------
if __name__ == "__main__":
    gcp.gcs_mount_bucket(logs_bucket_name, logs_path, ro=False)
    gcp.gcs_mount_bucket(data_in_bucket_name, data_in_path, ro=True)
    gcp.gcs_mount_bucket(data_out_bucket_name, data_out_path, ro=False)
    # gcp.gcs_mount_bucket(aa_bucket_name, aa_path, ro=True)
    # gcp.gcs_mount_bucket(imagery_in_bucket_name, imagery_in_path, ro=True)
    gcp.gcs_mount_bucket(imagery_meta_bucket_name, imagery_meta_path, ro=True)

    logging.basicConfig(
        filename=logs_path / log_file_name,
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.captureWarnings(True)
    logger.info("Beginning scheduled processing for %s", file_info)

    logger.info("Generating glider paths")
    # Generate glider paths
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
    logger.info("Generating timeseries netCDF files---------------------")
    outname_dict_ts = pipeline.generate_timeseries(
        deployment_name = deployment_name, 
        mode = mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_eng=write_nc,
        write_sci=write_nc,
        file_info=file_info,
        binary_search="*.[de]cd"
    )

    # Recalculate flbbcd values and correct cdom, if necessary
    if write_nc:
        logger.info("Correcting data---------------------")
        pipeline.correct_cdom_raw_sci(glider_paths=glider_paths)


    # logger.info("Generating gridded netCDF files---------------------")
    # outname_dict_gr = pipeline.generate_gridded(
    #     glider_paths=glider_paths,
    #     write_gridded=write_nc,
    # )

    # outname_dict = outname_dict_ts | outname_dict_gr


    #--------------------------------------------------------------------------
    # ### Ancillary data products
    # tssci = xr.load_dataset(outname_dict["outname_tssci"])
    # tseng = xr.load_dataset(outname_dict["outname_tseng"])
    # g5sci = xr.load_dataset(outname_dict["outname_5m"])

    # logger.info("Active Acoustics---------------------")
    # aa_paths = paths.get_path_aa(
    #     deployment_name, 
    #     mode, 
    #     aa_in_path=aa_in_path, 
    #     data_out_path=data_out_path, 
    # )
    # aa.ancillary_echoview(tssci, aa_paths)
    
    # logger.info("Imagery---------------------")
    # img_paths = paths.get_path_imagery(
    #     deployment_name = deployment_name, 
    #     imagery_in_path = imagery_in_path, 
    #     imagery_meta_path = imagery_meta_path, 
    #     data_out_path = data_out_path, 
    # )
    # imagery.imagery_timeseries(tssci, img_paths)

    #--------------------------------------------------------------------------
    # ### Plots
    # logger.info("Generating plots---------------------")
    # etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    # plots.esd_all_plots(
    #     outname_dict,
    #     crs="Mercator",
    #     base_path=glider_paths["plotdir"],
    #     bar_file=str(etopo_path),
    # )
    # ## OR, for Antarctic ##
    # plots.esd_all_plots(
    #     outname_dict, 
    #     crs=None, 
    #     base_path=glider_paths["plotdir"], 
    # )
    # plots.sci_surface_map_loop(
    #     xr.load_dataset(outname_dict["outname_gr5m"]),
    #     crs="Mercator",
    #     base_path=glider_paths["plotdir"],
    #     figsize_x=11,
    #     figsize_y=8.5,
    # )

    #--------------------------------------------------------------------------
    # ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    #     outname_dict["outname_tssci"], 
    #     glider_paths['profdir'], 
    #     glider_paths['deploymentyaml'],
    #     force=True, 
    # )

    #--------------------------------------------------------------------------
    logger.info("Completed scheduled processing")
