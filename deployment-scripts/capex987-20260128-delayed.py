import logging
from pathlib import Path

# import numpy as np
import xarray as xr

from esdglider import aa, gcp, imagery, paths, plots, utils
from esdglider.slocum import pipeline
from esdglider.slocum import core

logger = logging.getLogger(__name__)

### Variables for user to update
deployment_name = "capex987-20260128" #"amlr08-20220513"
mode = "delayed"
write_nc = True
prof_kwargs = {
    "length": 12,
}

### Consistent variables
# Define directories
# Change for local paths
home = Path("D:/esd data structure/")
# mnt_path = home / "gcs-mnt"
cac_path = "D:/esd data structure/cache/"
config_path = "deployment-configs/"

# Bucket names and paths
logs_bucket_name = "D:/esd data structure/logs"
data_in_bucket_name = "D:/esd data structure/data-in"
data_out_bucket_name = "D:/esd data structure/data-out"
# aa_bucket_name = "swfscesd-glider-active-acoustics-data-in"
# imagery_in_bucket_name = "swfscesd-glider-imagery-data-in"
# imagery_meta_bucket_name = "swfscesd-glider-imagery-metadata"

logs_path = Path(logs_bucket_name)
data_in_path = Path(data_in_bucket_name)
data_out_path = Path(data_out_bucket_name)

# Misc
file_info = f"https://github.com/SWFSC/glider-lab: {Path(__file__).stem}"
log_file_name = f"capex987-20260128-delayed.log"

#------------------------------------------------------------------------------
if __name__ == "__main__":
    # gcp.gcs_mount_bucket(logs_bucket_name, logs_path, ro=False)
    # gcp.gcs_mount_bucket(data_in_bucket_name, data_in_path, ro=True)
    # gcp.gcs_mount_bucket(data_out_bucket_name, data_out_path, ro=False)
    # gcp.gcs_mount_bucket(aa_in_bucket_name, aa_in_path, ro=True)
    # gcp.gcs_mount_bucket(imagery_in_bucket_name, imagery_in_path, ro=True)
    # gcp.gcs_mount_bucket(imagery_meta_bucket_name, imagery_meta_path, ro=True)

    logging.basicConfig(
        filename=logs_path / log_file_name,
        filemode="w",
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s [line %(lineno)d]",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.captureWarnings(True)
#    logger.info("Beginning scheduled processing for %s", file_info)
    logger.info("Beginning scheduled processing for %s", deployment_name)

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
    logger.info("Generating timeseries netCDF files---------------------")
    outname_dict_ts = pipeline.generate_timeseries(
        deployment_name = deployment_name, 
        mode = mode, 
        glider_paths=glider_paths,
        write_raw=write_nc,
        write_eng=write_nc,
        write_sci=write_nc,
        file_info=file_info,
    )

    # # Recalculate flbbcd values and correct cdom, if necessary
    # if write_nc:
    #     logger.info("Correcting data---------------------")
    #     pipeline.correct_flbbcd_raw_sci(glider_paths=glider_paths)
    #     pipeline.correct_cdom_raw_sci(glider_paths=glider_paths)

    # # Correct profiles, and make other adjustments to netCDF files
    if write_nc:
        tsraw = xr.load_dataset(outname_dict_ts["outname_tsraw"])
        tseng = xr.load_dataset(outname_dict_ts["outname_tseng"])
        tssci = xr.load_dataset(outname_dict_ts["outname_tssci"])

    # Implement specific checks, if needed, -8 for all after correction based on start of mission
    # 141 correction
    tsraw["profile_index"].loc[
        dict(time=slice("2026-02-06 22:00", "2026-02-06 22:30:45"))
    ] = 133

    # # 102 correction
    tsraw["profile_index"].loc[
        dict(time=slice("2026-02-03 13:01:33", "2026-02-03 13:32:00"))
    ] = 94.5

    # 155 correction
    tsraw["profile_index"].loc[
        dict(time=slice("2026-02-07 22:35", "2026-02-07 22:36:45"))
    ] = 146.5

    # 171 correction 
    tsraw["profile_index"].loc[
        dict(time=slice("2026-02-09 09:41", "2026-02-09 09:43"))
    ] = 162.5

    # Finish raw dataset work
    prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
    prof_summ.to_csv(glider_paths["profsummpath"], index=False)
    utils.check_profiles(prof_summ)
    tsraw.to_netcdf(
        outname_dict_ts["outname_tsraw"], 
        encoding={'time': pipeline.time_encoding}
    )

    # Apply new profiles to sci and eng
    tseng = utils.join_profiles(tseng, prof_summ, **prof_kwargs)
    tssci = utils.join_profiles(tssci, prof_summ, **prof_kwargs)
    tseng.to_netcdf(
        outname_dict_ts["outname_tseng"], 
        encoding={'time': pipeline.time_encoding}
        )
    tssci.to_netcdf(
        outname_dict_ts["outname_tssci"], 
        encoding={'time': pipeline.time_encoding}
        )
    logging.info("Completed adjustments")

# FROM AMLR 30
    # if write_nc:
    #     tsraw = xr.load_dataset(outname_dict_ts["outname_tsraw"])
    #     tseng = xr.load_dataset(outname_dict_ts["outname_tseng"])
    #     tssci = xr.load_dataset(outname_dict_ts["outname_tssci"])

    #     # Adjust profile index
    #     logging.info("Correcting profile_index for raw, eng, and sci datasets")
    #     # tssci["profile_index"].loc[dict(time="2024-11-13 15:14:59")] = 590.5
    #     tsraw["profile_index"].loc[
    #         dict(time=slice("2026-02-01 09:05", "2026-02-01 09:16:10"))
    #     ] = 397
    #     tsraw["profile_index"].loc[
    #         dict(time=slice("2026-01-24 00:03:07", "2026-01-24 00:04:10"))
    #     ] = 167
    #     tsraw["profile_index"].loc[
    #         dict(time=slice("2026-01-25 01:51", "2026-01-25 01:55"))
    #     ] = 182
        
    #     # Finish raw dataset work
    #     prof_summ = utils.calc_profile_summary(tsraw, "depth_measured")
    #     prof_summ.to_csv(glider_paths["profsummpath"], index=False)
    #     utils.check_profiles(prof_summ)
    #     tsraw.to_netcdf(
    #         outname_dict_ts["outname_tsraw"], 
    #         encoding={'time': pipeline.time_encoding}
    #     )

    #     # Apply new profiles to sci and eng
    #     tseng = utils.join_profiles(tseng, prof_summ, **prof_kwargs)
    #     tssci = utils.join_profiles(tssci, prof_summ, **prof_kwargs)
    #     tseng.to_netcdf(
    #         outname_dict_ts["outname_tseng"], 
    #         encoding={'time': pipeline.time_encoding}
    #     )
    #     tssci.to_netcdf(
    #         outname_dict_ts["outname_tssci"], 
    #         encoding={'time': pipeline.time_encoding}
    #     )
    #     logging.info("Completed adjustments")

    logger.info("Generating gridded netCDF files---------------------")
    outname_dict_gr = pipeline.generate_gridded(
        glider_paths=glider_paths,
        write_gridded=write_nc,
    )

    outname_dict = outname_dict_ts | outname_dict_gr


    #--------------------------------------------------------------------------
    ### Ancillary data products
    tssci = xr.load_dataset(outname_dict["outname_tssci"])
    tseng = xr.load_dataset(outname_dict["outname_tseng"])
    g5sci = xr.load_dataset(outname_dict["outname_gr5m"])

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
    ### Plots
    logger.info("Generating plots---------------------")
    etopo_path = home / "ETOPO_2022_v1_15s_N45W135_erddap.nc"
    plots.esd_all_plots(
        outname_dict,
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        # bar_file=str(etopo_path), # existing etopo path is for California
    )
    ## OR, for Antarctic ##
    # plots.esd_all_plots(
    #     outname_dict, 
    #     crs=None, 
    #     base_path=glider_paths["plotdir"], 
    # )
    plots.sci_surface_map_loop(
        xr.load_dataset(outname_dict["outname_gr5m"]),
        crs="Mercator",
        base_path=glider_paths["plotdir"],
        figsize_x=11,
        figsize_y=8.5,
    )

    #--------------------------------------------------------------------------
    ### Generate profile netCDF files for the DAC
    # glider.ngdac_profiles(
    core.ngdac_profiles(
        outname_dict["outname_tssci"], 
        glider_paths['profdir'], 
        glider_paths['deploymentyaml'],
        force=True, 
    )

    #--------------------------------------------------------------------------
    logger.info("Completed scheduled processing")
